# Adding path
import sys
sys.path.append("./")

import os
import openai
import random
from typing import List, Any, Union, Optional, Tuple, Dict
from Core.core import DATA_DIR,config # FST_INDICATION,SCD_INDICATION, 

class MarBot:
    """ An Example of COntinue Flow"""

    def __init__ (self, tasks):
        self.tasks = tasks
        self.code = random.randint(1, 10000)
        self.file_at = os.path.join(DATA_DIR, f"code_{self.code}.txt")
        self.unpack_keys()

    def unpack_keys (self):
        """ Unpack keys"""
        self.model = config.app_config_openai.model
        self.role, self.system , self.user, self.content, self.choices, self.message = config.app_config_openai.openai_keys
        self.executing, self.completed, self.error_max = config.app_config_other.other_messages
        self.chain_flows, self.fst_input, self.fst_output, self.snd_indication = config.app_config_other.chain_flows

    def _check_task (self) -> Union[bool, str]:
        """ Execute the First Command to check Libraries and tasks."""
        response = openai.ChatCompletion.create(
        model=self.model, # The deployment name you chose when you deployed the ChatGPT or GPT-4 model on the config.yml file
        messages=[
            {self.role:self.system,self.content: self.fst_input + self.chain_flows + self.fst_output,},
            {self.role:self.user,self.content: self.tasks}],temperature = 0)
        tasks = response[self.choices][0][self.message][self.content]

        # Check we have task on Memory
        if os.path.exists(self.file_at):
            pass
        else:
            print(self.executing)
            with open(self.file_at, "w") as fileTask:
                fileTask.write(tasks)

        return True, tasks
    
    def create_actions (self, actions:dict)-> str:
        """ Create the actions by the given computer language"""
        response = openai.ChatCompletion.create(
        model=self.model, messages=[
            {self.role:self.system,self.content: self.snd_indication},
            {self.role:self.user,self.content: actions}],temperature = 0)
        do =  response[self.choices][0][self.message][self.content]

        return do 

    def perform_action (self,action):
        """ Perform the action using exec """
        try:
            exec(action) 
            return True
        except Exception as e:
            return e
        
    def retry_action(self, action_func, parameter) -> None:
        """ Retry the action a maximum of 3 times """
        max_attempts = 3
        attempt = 1

        while attempt <= max_attempts:
            action_string = action_func(parameter)
            result = self.perform_action(action_string)
            if result is True:
                print(self.completed)
                break
            elif attempt == max_attempts:
                print(self.error_max)
                break
            attempt += 1

    def start_tasks (self) -> None:
        """ Start Tasks"""
        trigger, task_n = self._check_task()
        self.retry_action(self.create_actions, task_n)
