import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ToDOList(unittest.TestCase):
    url = 'https://todomvc.com/examples/react/'
    all_tasks = ('a', 'b', 'c')
    completed_tasks_index = (1,)
    completed_tasks_name = ('b',)
    active_tasks = ('a', 'c')

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)


    def test_todo_list(self):
        self.assertIn("React • TodoMVC", self.browser.title)
        # create tasks and check
        element = self.get_elements_by_css_selector("header.header>input.new-todo")[0]
        self.create_tasks(element)
        todo_list = self.get_elements_by_css_selector("ul.todo-list>li")
        self.check_tasks(todo_list)

        # find filters tabs
        self.filters = self.browser.find_elements_by_css_selector('ul.filters>li')

        # complete tasks and check
        self.complete_tasks(todo_list)
        self.check_complete_tasks(todo_list)

        # check active tasks
        self.check_active_tasks()


    def tearDown(self):
        self.browser.close()

    def create_tasks(self, element):
        for task in self.all_tasks:
            element.send_keys(task)
            element.send_keys(Keys.RETURN)


    def complete_tasks(self, todo_list):
        for task in self.completed_tasks_index:
            todo_list[task].find_element_by_tag_name('input').click()

    def get_elements_by_css_selector(self, css_selector):
        elements = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector))
        )
        return elements

    def check_tasks(self, todo_list):
        generator_tasks = (div.find_element_by_tag_name('label').text for div in todo_list)
        text_tasks = tuple(generator_tasks)
        self.assertEqual(self.all_tasks, text_tasks)

        # check display count tasks
        # count_tasks = int(self.browser.find_element_by_css_selector('span.todo-count>strong').text)
        # assert len(text_tasks) == count_tasks

    def check_complete_tasks(self, todo_list):
        # check class completed
        # for task in self.completed_tasks_index:
        #     assert todo_list[task].get_attribute("class") != 'completed'

        # open tab Completed
        self.filters[2].click()
        completed_tasks = self.get_elements_by_css_selector('ul.todo-list>li>div.view>label')
        generator_tasks = (task.text for task in completed_tasks)
        text_tasks = tuple(generator_tasks)
        self.assertEqual(text_tasks, self.completed_tasks_name)

    def check_active_tasks(self):
        # open tab Active
        self.filters[1].click()
        active = self.get_elements_by_css_selector('ul.todo-list>li>div.view>label')
        generator_active = [label.text for label in active]
        text_active = tuple(generator_active)
        self.assertEqual(text_active, self.active_tasks)
if __name__ == "__main__":
    unittest.main()