import pytest
from model import Question


@pytest.fixture
def question():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.add_choice('d')
    question.add_choice('e')
    return question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_long_valid_title():
    question = Question(title='a'*200)
    assert question.title == 'a'*200

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)
    with pytest.raises(Exception):
        Question(title='q1', points=-1)

def test_create_no_choice():    
    question = Question(title='q1')
    assert question.choices == []

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    
    with pytest.raises(Exception):
        question.add_choice('', False)
    with pytest.raises(Exception):
        question.add_choice('a'*101, False)

def test_create_multiple_choices():
    question = Question(title='q1')

    question.add_choice('a', True)
    question.add_choice('b', False)
    
    assert len(question.choices) == 2

    choice1 = question.choices[0]
    assert choice1.text == 'a'
    assert choice1.is_correct

    choice2 = question.choices[1]
    assert choice2.text == 'b'
    assert not choice2.is_correct

def test_remove_single_choice():
    question = Question(title='q1')
    question.add_choice(['a', True])
    question.add_choice(['b', False])
    question.add_choice(['c', False])

    question.remove_choice_by_id(1)

    assert len(question.choices) == 2

def test_remove_multiple_choices():
    question = Question(title='q1')
    question.add_choice(['a', True])
    question.add_choice(['b', False])
    question.add_choice(['c', False])

    question.remove_choice_by_id(1)
    question.remove_choice_by_id(2)

    assert len(question.choices) == 1

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice(['a', True])
    question.add_choice(['b', False])
    question.add_choice(['c', False])

    question.remove_all_choices()

    assert len(question.choices) == 0

def test_remove_invalid_choice():
    question = Question(title='q1')
    question.add_choice(['a', True])
    question.add_choice(['b', False])

    with pytest.raises(Exception):
        question.remove_choice_by_id(100)

def test_choice_id_increments_basic():
    question = Question(title='q1')

    question.add_choice(['a', True])
    question.add_choice(['b', False])
    question.add_choice(['c', False])

    choice1 = question.choices[0]
    choice2 = question.choices[1]
    choice3 = question.choices[2]

    assert choice1.id == 1
    assert choice2.id == 2
    assert choice3.id == 3

def test_choice_id_increments_add_remove():
    question = Question(title='q1')
    
    question.add_choice(['a', True])
    question.add_choice(['b', False])
    question.add_choice(['c', False])
    question.remove_choice_by_id(1)

    choice1 = question.choices[0]
    choice2 = question.choices[1]

    assert len(question.choices) == 2
    assert choice1.id == 2
    assert choice2.id == 3

def test_choice_id_increments_add_remove_add():
    question = Question(title='q1')
    
    question.add_choice(['a', True])
    question.add_choice(['b', False])
    question.add_choice(['c', False])
    question.remove_choice_by_id(1)
    question.add_choice('d', False)

    choice1 = question.choices[0]
    choice2 = question.choices[1]
    choice3 = question.choices[2]

    assert len(question.choices) == 3
    assert choice1.id == 2
    assert choice2.id == 3
    assert choice3.id == 4

def test_select_one_correct_choice(question):
    question.set_correct_choices([1])
    assert question.select_choices([1]) == [1]

def test_select_multiple_correct_choices(question):

    question.max_selections = 5

    question.set_correct_choices([1,2])
    assert question.select_choices([1,2]) == [1,2]

    question.set_correct_choices([1,2,3,4,5])
    assert question.select_choices([1,2,3,4,5]) == [1,2,3,4,5]

def test_max_selections_exceeded(question):
    
    question.max_selections = 2

    with pytest.raises(Exception):
        question.select_choices([1,2,3])

def test_select_one_incorrect_choice(question):

    question.set_correct_choices([1])
    assert question.select_choices([2]) == []
    assert question.select_choices([3]) == []
    assert question.select_choices([4]) == []
    assert question.select_choices([5]) == []

def test_select_multiple_incorrect_choices(question):

    question.set_correct_choices([1,2])

    question.max_selections = 3
    assert question.select_choices([3,4]) == []
    assert question.select_choices([3,5]) == []
    assert question.select_choices([3,4,5]) == []

def test_select_mixed_choices(question):

    question.max_selections = 5

    question.set_correct_choices([1,2])

    assert question.select_choices([1,3]) == [1]
    assert question.select_choices([1,4]) == [1]
    assert question.select_choices([1,5]) == [1]
    assert question.select_choices([1,3,4]) == [1]
    assert question.select_choices([1,3,4,5]) == [1]

    question.set_correct_choices([1,2,3])

    assert question.select_choices([2,3,4,5]) == [2,3]
    assert question.select_choices([1,2,3,4,5]) == [1,2,3]