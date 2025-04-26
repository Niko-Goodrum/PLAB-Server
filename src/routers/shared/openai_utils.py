import logging
import re
from pyexpat.errors import messages

import openai
from openai import OpenAIError, OpenAI

from enum import Enum

from src.config import Config
from src.routers.interview.enums import InterviewType
from src.routers.interview.exceptions import InvalidInerviewType, NoAnswer

client = OpenAI(
    api_key=Config.OPENAI_KEY,
    base_url="https://models.github.ai/inference",
)

async def post_openai(system_content, user_content):
    try:

        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            temperature=0.8
        )
        answer = response.choices[0].message.content

        return answer


    except openai.OpenAIError as e:
        logging.exception(e)
        return None

def make_prompt(type: InterviewType) -> str:
    prompt = "한국어로 답변해주세요; "

    if type == InterviewType.Tech:
        prompt += """당신은 개발자를 뽑는 **기술 면접관**입니다. 지금부터 신입 개발자와의 면접을 진행합니다. 다음 규칙을 따르세요:
                    1. 기술적인 능력을 평가하는 데 집중하세요. 전공지식, 프로젝트 경험, 문제 해결 능력, 사용 가능한 기술 스택을 중심으로 질문하세요.
                    2. 질문은 기본적인 수준에서 시작해 점점 심화된 질문으로 발전시켜 주세요.
                    3. 기술 선택의 이유, 실무에 적용했던 경험, 코드 구조, 협업 중 겪은 기술 이슈 등도 질문하세요.
                    4. 너무 어렵거나 모를 수도 있는 질문에는 힌트를 주거나 유도 질문을 활용하세요.
                    5. 질문은 한 번에 하나씩만 하세요.
                    6. 답변 이후, 간단한 피드백이나 후속 질문을 해주세요."""

    elif type == InterviewType.Behavioral:
        prompt += """당신은 신입 개발자를 평가하는 **인성 면접관**입니다. 인성과 소프트 스킬 중심으로 면접을 진행합니다. 다음 규칙을 따르세요:
                    1. 지원자의 커뮤니케이션 능력, 태도, 동기, 협업 경험, 문제 해결 방식 등을 중심으로 질문하세요.
                    2. 상황 기반 질문(Situation-Task-Action-Result, STAR)을 활용하세요.
                    3. 스트레스 상황, 갈등 해결, 실패 경험, 리더십 경험, 동기부여에 대한 질문을 포함하세요.
                    4. 너무 개인적인 질문은 피하고, 직무와 관련된 태도 중심으로 질문하세요.
                    5. 질문은 하나씩, 대화형으로 이어가세요.
                    6. 답변 후에는 공감하거나 간단한 피드백을 주되, 객관성을 유지하세요."""

    elif type == InterviewType.Total:
        prompt += """당신은 신입 개발자를 평가하는 **면접관**입니다. 기술적 역량과 인성 모두를 평가하는 종합 면접을 진행합니다. 다음 규칙을 따르세요:
                    1. 면접은 자기소개 → 인성 질문 → 기술 질문 → 마무리 순으로 진행하세요.
                    2. 인성 질문에서는 협업, 커뮤니케이션, 동기, 문제 해결 방식 등을 파악하세요.
                    3. 기술 질문에서는 사용 기술, 프로젝트 경험, 로직 이해도, 코드 설계 등을 확인하세요.
                    4. 질문은 항상 한 번에 하나씩만 하고, 응답을 기다린다는 가정 하에 진행하세요.
                    5. 필요 시 꼬리 질문이나 사례 기반 질문으로 심화 질문을 이어가세요.
                    6. 친절하고 자연스럽게 질문하면서도 면접관으로서의 객관성을 유지하세요."""

    else:
        raise InvalidInerviewType

    return prompt


async def create_interview_prompt(last_question = None, last_answer = None, type: InterviewType = None):
    system_content = "You are a helpful consulting assistant."


    prompt = make_prompt(type)

    prompt += """
    첫번째 문장에는 답변에 대한 피드백을 포함해주세요.
    두번째 문장에는 다음 질문은 이어가주세요.
    """

    if last_question is not None:
        prompt += f"""
        면접관의 전 질문은 
        {last_question}
        입니다. 
        """

    question = await post_openai(system_content, prompt + last_answer)

    if question is None:
        raise NoAnswer

    sentences = re.split('\n', question)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    return sentences

