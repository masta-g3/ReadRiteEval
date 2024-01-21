from pydantic import BaseModel, Field, conlist
from typing import Optional, Tuple
from enum import Enum

class TestNames(str, Enum):
    spatial_reasoning = "spatial_reasoning"
    sequence_logic_puzzle = "sequence_logic_puzzle"
    dependency_cascades = "dependency_cascades"
    hypothesis_testing = "hypothesis_testing"
    contextual_dissonance = "contextual_dissonance"


# class ModelNames(str, Enum):
#     gpt_35_turbo = "gpt-3.5-turbo-1106"
#     gpt_4_turbo = "gpt-4-1106-preview"
#     una_cybertron_7b_v2 = "una-cybertron-7b-v2-bf16"
#     open_hermes_neural_7b_chat = "openhermes-2.5-neural-chat-7b-v3-1-7b"
#     mistral_7b_instruct_v02 = "mistral-7b-instruct-v0.2"
#     mixtral_8x7b_instruct_v01 = "Mixtral-8x7B-Instruct-v0.1"
#     nous_hermes_mixtral_8x7b_sft_v2 = "Nous-Hermes-2-Mixtral-8x7B-SFT"
#     code_llama_7b_instruct = "CodeLlama-7b-Instruct"
#     qwen_7b_chat = "Qwen-7B-Chat"
#     phi_2 = "phi-2"

class TestScore(BaseModel):
    test: TestNames = Field(description="Name of the test.")
    model: str = Field(description="Name of the model.")
    individual_scores: conlist(bool, min_length=1) = Field(description="Scores for each individual question.")
    total_score: float = Field(description="Score for the test.")
    full_answers: Optional[conlist(str)] = Field([], description="Answers for each individual question.")
    full_validations: Optional[conlist(object)] = Field([], description="Validations for each individual question.")


###########################
## SEQUENCE LOGIC PUZZLE ##
###########################
class PuzzleValidator(BaseModel):
    analysis: str = Field(description="Detailed analysis of the proposed answer.")
    valid: bool = Field(description="Whether the proposed answer is valid given the rules.")


class Puzzle(BaseModel):
    rules: str = Field(description="Rules to build a sequence. Must include emojis encoded as UTF-8.")
    answer: str = Field(description="Proposed answer to the puzzle (must be unique).")
    validation: Optional[PuzzleValidator] = None

    def validation_prompt(self):
        return f""" Below you will be presented with rules to build a sequence and a proposed answer. Your task is to determine if the answer is valid given the rules. First analyze carefully the sequence and if it complies with the rules, then determine its valid status. You must also make sure that the proposed answer is the only possible answer. If there are other possible answers, the proposed answer is invalid.
RULES: {self.rules}
PROPOSED ANSWER: {self.answer}"""

    def question_prompt(self):
        return f""" Your task is to solve a logical puzzle. Below is a sample puzzle and its corresponding answer.

EXAMPLE RULES:
In this puzzle, ue the symbols 🐶 (Dog), 🍖 (Bone), 🐾 (Paw Print), 🎾 (Tennis Ball), 🥇 (Medal), and 🌳 (Tree).
1. 🐶 cannot be directly before or after 🎾.
2. 🍖 must always precede 🐾 but follow 🐶.
3. 🎾 must be immediately after 🐾.
4. The sequence must start with 🐶.
5 🌳 cannot be adjacent to either 🐶 or 🍖.
6. The sequence contains exactly one of each symbol.
7. 🥇 must be the last in the sequence.

EXAMPLE ANSWER: 🐶, 🍖, 🐾, 🎾, 🌳, 🥇

No read carefully over the following rules. Reply ONLY with the correct sequence of emojis and no other comment.
RULES: 
{self.rules}

ANSWER:"""


###########################
## CONTEXTUAL DISSONANCE ##
###########################

class PassageTopicList(BaseModel):
    topics: conlist(str, min_length=30, max_length=70) = Field(description="List of 50 topics.")


class ContextualPassage(BaseModel):
    topic: str = Field(description="Topic of the passage.")
    irrelevant_topic: str = Field(description="Topic that is irrelevant to the passage, but seems superficially related (i.e.: close in embedding space).")
    passage: str = Field(description="Passage that is relevant to the topic.")
    irrelevant_sentence: str = Field(description="Sentence that is irrelevant to the topic.")

    def question_prompt(self):
        return f""" Your task is to read over the following passage about '{self.topic}' and determine which of its sentences is irrelevant to the topic. Below is a sample passange and its corresponding passage.
        
EXAMPLE PASSAGE:
War has significantly shaped the course of human history, influencing societal development and geopolitical landscapes. The tactics and technologies of warfare have evolved dramatically, from ancient hand-to-hand combat to modern-day cyber warfare. These conflicts often lead to major social and political changes, such as the rise and fall of empires, shifts in power dynamics, and alterations in national boundaries. Despite the devastation, war has also been a catalyst for technological advancement and strategic thinking. The process of industrialization has paralleled many historical conflicts, reflecting how societies adapt to and are shaped by the pressures of war. The consequences of war extend beyond the battlefield, affecting civilian life, economic structures, and cultural norms.

EXAMPLE ANSWER: The process of industrialization has paralleled many historical conflicts, reflecting how societies adapt to and are shaped by the pressures of war.


Now read carefully over the following passage.

PASSAGE:
{self.passage}

Reply ONLY with the irrelevant sentence and no other comment or explanation.    
ANSWER:"""


#######################
## SPATIAL REASONING ##
#######################

class CityNameList(BaseModel):
    city_names: conlist(str, min_length=80, max_length=150) = Field(
        description="List of 100 imaginary thematic city names.")


class CityQnaValidator(BaseModel):
    analysis: str = Field(description="Detailed analysis of the proposed answer.")
    valid: bool = Field(description="Whether the proposed answer is valid given the rules.")


class CityQnA(BaseModel):
    question: str = Field(description="Question on how to navigate the city.")
    answer: str = Field(description="Answer to the question, following the specified syntax.")
    validation: Optional[CityQnaValidator] = None

    def validation_prompt(self, city_layout, answer=None):

        if answer is None:
            answer = self.answer
        return f""" Below you will be presented with a city layout, a question about how to navigate it and an answer to that question. Your task is to determine if the answer is valid given the city layout. The answer must be in the form of a sequence of actions using the format: ACTION (detail). Actions include WALK (street or area), TURN (direction at a landmark), and REACH (destination). Separate each action with '->'. If a route is not possible, the answer should be 'NOT POSSIBLE'.
CITY LAYOUT: {city_layout}

QUESTION: {self.question}

ANSWER: {answer}"""

    def question_prompt(self, city_layout):
        return f""" Your task is to read over the following city layout and answer a question on how to navigate it. Your answer must be in the form of a sequence of actions using the format: ACTION (detail). Actions include WALK (street or area), TURN (direction at a landmark), and REACH (destination). Separate each action with '->'. If a route is not possible, answer with 'NOT POSSIBLE'. Reply only with the answer and no other comment or explanation. 

EXAMPLE ANSWER: WALK Main Street -> TURN right at the fountain -> WALK the park -> REACH the library

CITY LAYOUT:
{city_layout}

QUESTION: {self.question}

ANSWER:"""


class City(BaseModel):
    name: str = Field(description="Name of the city.")
    description: str = Field(description="Detailed description of the city layout.")
    qna: conlist(CityQnA, min_length=1, max_length=10) = Field(
        description="Questions and answers about the city layout.")