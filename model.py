import uuid
            

class Choice:

    def __init__(self, id: int, text: str, is_correct: bool = False):

        if len(text) == 0:
            raise Exception('Text cannot be empty')
        if len(text) > 100:
            raise Exception('Text cannot be longer than 100 characters')

        self.id = id
        self.text = text
        self.is_correct = is_correct

class Question:

    def __init__(self, title: str, points: int=1, max_selections: int=1):

        if len(title) == 0:
            raise Exception('Title cannot be empty')
        if len(title) > 200:
            raise Exception('Title cannot be longer than 200 characters')
        if points < 1 or points > 100:
            raise Exception('Points must be between 1 and 100')

        self.title = title
        self.points = points
        self.max_selections = max_selections

        self.id = uuid.uuid4().hex
        self.choices = []

    def add_choice(self, text: str, is_correct: bool = False) -> Choice:
        choice = self._create_choice(text, is_correct)
        self.choices.append(choice)
        return choice
    
    def remove_choice_by_id(self, id: int):
        choice = self._choice_by_id(id)
        self.choices.remove(choice)
    
    def remove_all_choices(self):
        self.choices.clear()

    def select_choices(self, selected_choice_ids: list[int]) -> list[int]:
        
        if len(selected_choice_ids) > self.max_selections:
            raise Exception(f'Cannot select more than {self.max_selections} choices')
        
        return [selected_choice_id for selected_choice_id in selected_choice_ids if selected_choice_id in self._correct_choice_ids()]
    
    def set_correct_choices(self, correct_choice_ids: list[int]):
        for choice_id in correct_choice_ids:
            choice = self._choice_by_id(choice_id)
            if choice:
                choice.is_correct = True

    def _create_choice(self, text, is_correct):
        return Choice(id=self._generate_choice_id(), text=text, is_correct=is_correct)
    
    def _choice_ids(self):
        return [choice.id for choice in self.choices]
    
    def _correct_choice_ids(self) -> list[int]:
        return [choice.id for choice in self.choices if choice.is_correct]
    
    def _choice_by_id(self, choice_id: str):
        self._check_valid_choice_id(choice_id)
        for choice in self.choices:
            if choice.id == choice_id:
                return choice
            
    def _check_valid_choice_id(self, choice_id):
        if choice_id not in self._choice_ids():
            raise Exception(f'Invalid choice id {choice_id}')

    def _generate_choice_id(self) -> int:
        if len(self.choices) == 0:
            return 1
        last_choice = self.choices[-1]
        return last_choice.id + 1
        