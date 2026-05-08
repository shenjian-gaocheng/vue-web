import html
import os
import re
from datetime import datetime, timezone
from html.parser import HTMLParser

from extensions import BASE_DIR, PROJECT_ROOT
from models import Event, Stage


BAIKE_FILE_PATH = os.path.join(PROJECT_ROOT, 'src', 'pages', 'Baike.vue')
KNOWLEDGE_FALLBACK_MESSAGE = '抱歉，我只能回答知识库中已有的信息。'
KNOWLEDGE_BASE = {
    'documents': [],
    'built_at': None,
    'stats': {
        'baike_documents': 0,
        'stage_documents': 0,
        'event_documents': 0,
        'total_documents': 0,
    },
}


class VueTemplateTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.texts.append(text)


def normalize_whitespace(value):
    return re.sub(r'\s+', ' ', str(value or '')).strip()


def chunk_text(text, max_length=240):
    segments = [normalize_whitespace(item) for item in text.splitlines() if normalize_whitespace(item)]
    chunks = []
    buffer = ''

    for segment in segments:
        candidate = f'{buffer} {segment}'.strip() if buffer else segment
        if len(candidate) <= max_length:
            buffer = candidate
            continue

        if buffer:
            chunks.append(buffer)
        buffer = segment

    if buffer:
        chunks.append(buffer)

    return chunks


def extract_baike_documents():
    if not os.path.exists(BAIKE_FILE_PATH):
        return []

    with open(BAIKE_FILE_PATH, 'r', encoding='utf-8') as file:
        content = file.read()

    template_match = re.search(r'<template>(.*?)</template>', content, flags=re.S)
    template = template_match.group(1) if template_match else content
    template = re.sub(r'<!--.*?-->', ' ', template, flags=re.S)

    extractor = VueTemplateTextExtractor()
    extractor.feed(template)

    seen = set()
    visible_lines = []
    for raw_text in extractor.texts:
        text = normalize_whitespace(html.unescape(raw_text))
        if len(text) < 2 or text in seen:
            continue
        seen.add(text)
        visible_lines.append(text)

    chunks = chunk_text('\n'.join(visible_lines))
    return [
        {
            'id': f'baike-{index}',
            'source_type': 'baike',
            'source_label': 'Baike.vue',
            'title': f'小周百科片段 {index}',
            'content': chunk,
            'search_text': chunk.lower(),
        }
        for index, chunk in enumerate(chunks, start=1)
    ]


def serialize_stage_document(stage):
    status_text = '已结束' if stage.is_end else '进行中或未结束'
    kind_text = '公演' if stage.is_stage else '活动'
    content = normalize_whitespace(
        f'演出日期 {stage.date}，场次 {stage.session}，分类 {stage.type}，'
        f'代码 {stage.stage_code}，标题 {stage.title}，地点 {stage.time or "未提供"}，'
        f'记录类型 {kind_text}，状态 {status_text}。'
    )
    return {
        'id': f'stage-{stage.id}',
        'source_type': 'stage',
        'source_label': f'Stage#{stage.id}',
        'title': stage.title,
        'content': content,
        'search_text': f'{stage.title} {stage.type} {stage.stage_code} {content}'.lower(),
    }


def serialize_event_document(event):
    detail = normalize_whitespace(event.detail)
    content = normalize_whitespace(
        f'事件日期 {event.date}，标题 {event.title}，'
        f'重要事件 {"是" if event.is_imp else "否"}，详情 {detail or "未提供"}。'
    )
    return {
        'id': f'event-{event.id}',
        'source_type': 'event',
        'source_label': f'Event#{event.id}',
        'title': event.title,
        'content': content,
        'search_text': f'{event.title} {detail} {content}'.lower(),
    }


def build_knowledge_base():
    baike_documents = extract_baike_documents()
    stage_documents = [
        serialize_stage_document(stage)
        for stage in Stage.query.order_by(Stage.date.desc(), Stage.session.desc()).all()
    ]
    event_documents = [
        serialize_event_document(event)
        for event in Event.query.order_by(Event.date.desc()).all()
    ]

    documents = baike_documents + stage_documents + event_documents
    KNOWLEDGE_BASE['documents'] = documents
    KNOWLEDGE_BASE['built_at'] = datetime.now(timezone.utc).isoformat()
    KNOWLEDGE_BASE['stats'] = {
        'baike_documents': len(baike_documents),
        'stage_documents': len(stage_documents),
        'event_documents': len(event_documents),
        'total_documents': len(documents),
    }
    return KNOWLEDGE_BASE


def ensure_knowledge_base():
    if KNOWLEDGE_BASE['documents']:
        return KNOWLEDGE_BASE
    return build_knowledge_base()


def extract_query_terms(question):
    normalized_question = normalize_whitespace(question).lower()
    terms = set(re.findall(r'[a-z0-9]{2,}|[\u4e00-\u9fff]{2,}', normalized_question))

    for term in list(terms):
        if re.fullmatch(r'[\u4e00-\u9fff]{4,}', term):
            for index in range(len(term) - 1):
                terms.add(term[index:index + 2])

    return normalized_question, sorted(terms, key=len, reverse=True)


def score_document(question, terms, document):
    score = 0
    haystack = document['search_text']
    title = document['title'].lower()

    if question and question in haystack:
        score += 12

    for term in terms:
        if term in haystack:
            score += min(len(term), 6)
            if term in title:
                score += 2

    return score


def search_knowledge_base(question, top_k=5):
    knowledge_base = ensure_knowledge_base()
    normalized_question, terms = extract_query_terms(question)
    top_k = max(1, min(int(top_k or 5), 8))

    scored_documents = []
    for document in knowledge_base['documents']:
        score = score_document(normalized_question, terms, document)
        if score > 0:
            scored_documents.append({**document, 'score': score})

    scored_documents.sort(key=lambda item: item['score'], reverse=True)
    matched_documents = scored_documents[:top_k]
    is_relevant = bool(matched_documents) and matched_documents[0]['score'] >= 6
    return matched_documents, is_relevant


def get_deepseek_client():
    api_key = os.environ.get('sk-4287651d70084470896da519ac36f98e')
    if not api_key:
        raise RuntimeError('缺少 DEEPSEEK_API_KEY 环境变量，无法调用知识库模型。')

    try:
        from openai import OpenAI
    except ImportError as error:
        raise RuntimeError('缺少 openai 依赖，请先执行 pip3 install openai。') from error

    return OpenAI(
        api_key=api_key,
        base_url=os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
    )


def generate_knowledge_answer(question, matched_documents):
    context_blocks = []
    for index, document in enumerate(matched_documents, start=1):
        context_blocks.append(
            f'[{index}] 来源类型: {document["source_type"]} | 来源: {document["source_label"]} | 标题: {document["title"]}\n'
            f'{document["content"]}'
        )

    client = get_deepseek_client()
    response = client.chat.completions.create(
        model=os.environ.get('DEEPSEEK_MODEL', 'deepseek-v4-pro'),
        messages=[
            {
                'role': 'system',
                'content': (
                    '你是一个严格受知识库约束的问答助手。你只能基于提供的知识库片段回答。'
                    f'如果知识库片段不足以直接回答，请只输出：{KNOWLEDGE_FALLBACK_MESSAGE}'
                )
            },
            {
                'role': 'user',
                'content': (
                    f'用户问题：{question}\n\n'
                    '知识库片段如下：\n'
                    f'{os.linesep.join(context_blocks)}\n\n'
                    '回答要求：1. 仅依据片段回答。2. 不要补充外部常识。3. 若无法确认就直接拒答。'
                )
            },
        ],
        stream=False,
        reasoning_effort=os.environ.get('DEEPSEEK_REASONING_EFFORT', 'high'),
        extra_body={'thinking': {'type': 'enabled'}}
    )

    answer = normalize_whitespace(response.choices[0].message.content if response.choices else '')
    return answer or KNOWLEDGE_FALLBACK_MESSAGE
