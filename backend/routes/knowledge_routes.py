import logging

from flask import g
from flask import request
from flask_restx import Resource

from auth_utils import get_client_ip, token_required
from extensions import app, ns
from knowledge_base import (
    KNOWLEDGE_FALLBACK_MESSAGE,
    build_knowledge_base,
    ensure_knowledge_base,
    generate_knowledge_answer,
    search_knowledge_base,
)
from schemas import knowledge_chat_model


@ns.route('/knowledge-base/status')
class KnowledgeBaseStatus(Resource):
    @token_required
    def get(self):
        knowledge_base = ensure_knowledge_base()
        return {
            'built_at': knowledge_base['built_at'],
            'stats': knowledge_base['stats'],
        }, 200


@ns.route('/knowledge-base/rebuild')
class KnowledgeBaseRebuild(Resource):
    @token_required
    def post(self):
        if g.username not in app.config['ADMIN_USERS']:
            return {'message': '没有权限重建知识库'}, 403

        knowledge_base = build_knowledge_base()
        logging.info(f'用户: {g.username} 重建知识库，文档数: {knowledge_base["stats"]["total_documents"]}，IP: {get_client_ip()}')
        return {
            'message': '知识库已重建',
            'built_at': knowledge_base['built_at'],
            'stats': knowledge_base['stats'],
        }, 200


@ns.route('/knowledge-base/chat')
class KnowledgeBaseChat(Resource):
    @ns.expect(knowledge_chat_model)
    @token_required
    def post(self):
        data = request.json or {}
        question = str(data.get('question') or '').strip()
        top_k = data.get('top_k', 5)

        if not question:
            return {'message': 'question 不能为空'}, 400

        matched_documents, is_relevant = search_knowledge_base(question, top_k=top_k)
        if not is_relevant:
            return {
                'answer': KNOWLEDGE_FALLBACK_MESSAGE,
                'matched_sources': [],
                'used_model': False,
            }, 200

        try:
            answer = generate_knowledge_answer(question, matched_documents)
        except RuntimeError as error:
            return {'message': str(error)}, 500
        except Exception as error:
            logging.exception('知识库模型调用失败')
            return {'message': f'知识库模型调用失败: {str(error)}'}, 502

        return {
            'answer': answer,
            'matched_sources': [
                {
                    'id': document['id'],
                    'source_type': document['source_type'],
                    'source_label': document['source_label'],
                    'title': document['title'],
                    'score': document['score'],
                }
                for document in matched_documents
            ],
            'used_model': True,
        }, 200