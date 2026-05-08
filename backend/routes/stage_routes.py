from datetime import datetime

import logging
from flask import g
from flask import request
from flask_restx import Resource

from auth_utils import get_client_ip, token_required
from extensions import db, ns
from models import Stage
from schemas import stage_model


@ns.route('/stages')
class StageList(Resource):
    @ns.marshal_list_with(stage_model)
    @ns.doc(security=None)
    def get(self):
        return Stage.query.all()

    @ns.expect(stage_model)
    @token_required
    def post(self):
        data = request.json or {}
        stage = Stage(
            session=int(data['session']),
            date=data['date'],
            type=data['type'],
            stage_code=data['stage_code'],
            title=data['title'],
            url=data['url'],
            cut_url=data['cut_url'],
            time=data['time'],
            is_stage=data['is_stage'],
            is_end=data['is_end'],
        )
        db.session.add(stage)
        db.session.commit()

        logging.info(f'用户: {g.username} 添加演出记录: {data["session"]} {data["title"]}，IP: {get_client_ip()}')
        return {'message': '演出记录已添加'}, 201


@ns.route('/stages/<int:id>')
class StageItem(Resource):
    @ns.expect(stage_model)
    @token_required
    def put(self, id):
        data = request.json or {}
        stage = db.session.get(Stage, id)

        if not stage:
            return {'error': '找不到该演出记录'}, 404

        try:
            stage.session = int(data['session'])
            stage.date = data['date']
            stage.type = data['type']
            stage.stage_code = data['stage_code']
            stage.title = data['title']
            stage.url = data['url']
            stage.cut_url = data['cut_url']
            stage.time = data['time']
            stage.is_stage = data['is_stage']
            stage.is_end = data['is_end']

            db.session.commit()

            logging.info(f'用户: {g.username} 更新演出记录: {data["session"]} {data["title"]}，IP: {get_client_ip()}')
            return {'message': '演出记录已更新'}, 200
        except (KeyError, ValueError) as error:
            return {'error': f'更新失败: {str(error)}'}, 400


@ns.route('/stages/batch')
class StageBatch(Resource):
    @ns.expect([stage_model])
    @token_required
    def post(self):
        data_list = request.json

        if not isinstance(data_list, list):
            return {'error': '请求体应为 JSON 数组'}, 400

        stages = []
        for index, data in enumerate(data_list):
            try:
                date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
                stage = Stage(
                    session=int(data['session']),
                    date=date_obj,
                    type=data['type'],
                    stage_code=data['stage_code'],
                    title=data['title'],
                    url=data['url'],
                    cut_url=data['cut_url'],
                    is_stage=data['is_stage'],
                    is_end=data['is_end'],
                    time=data['time'],
                )
                stages.append(stage)
            except (KeyError, ValueError) as error:
                return {'error': f'第 {index + 1} 条数据有误: {str(error)}'}, 400

        db.session.add_all(stages)
        db.session.commit()

        logging.info(f'用户: {g.username} 添加 {len(stages)} 条演出记录，IP: {get_client_ip()}')
        return {'message': f'成功添加 {len(stages)} 条演出记录'}, 201