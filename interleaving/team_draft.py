from .ranking import Ranking
from .interleaving_method import InterleavingMethod
import numpy as np
from collections import defaultdict

class TeamDraft(InterleavingMethod):
    '''
    Team Draft Interleaving
    '''
    def interleave(self, a, b):
        '''
        a: a list of document IDs
        b: a list of document IDs

        Return an instance of Ranking
        '''
        return self.multileave(a, b)

    def multileave(self, *lists):
        '''performs multileaving...

        *lists: lists of document IDs

        Returns an instance of Ranking
        '''
        k = min(map(lambda l: len(l), lists))
        result = Ranking()
        teams = {}
        for i in range(len(lists)):
            teams[i] = set()
        empty_teams = set()

        while len(result) < k:
            selected_team = self._select_team(teams, empty_teams)
            docs = [x for x in lists[selected_team] if not x in result]
            if len(docs) > 0:
                selected_doc = docs[0]
                result.append(selected_doc)
                teams[selected_team].add(selected_doc)
            else:
                empty_teams.add(selected_team)

        result.teams = teams
        return result

    def _select_team(self, teams, empty_teams):
        team_lens = [len(teams[i]) for i in teams if not i in empty_teams]
        if len(team_lens) == 0:
            return None
        min_team_num = min(team_lens)
        available_teams = [i for i in teams
            if len(teams[i]) == min_team_num and not i in empty_teams]
        if len(available_teams) == 0:
            return None
        selected_team = np.random.choice(available_teams)
        return selected_team

    def evaluate(self, ranking, clicks):
        '''
        ranking: an instance of Ranking generated by Balanced.interleave
        clicks: a list of indices clicked by a user

        Return a list in which element (i, j) indicates i won j:
        '''
        team_num = len(ranking.teams)
        result = []
        if len(clicks) == 0:
            return result
        scores = {i: len([c for c in clicks if ranking[c] in ranking.teams[i]])
            for i in ranking.teams}

        for i in range(team_num):
            for j in range(i+1, team_num):
                if scores[i] > scores[j]:
                    result.append((i, j))
                elif scores[i] < scores[j]:
                    result.append((j, i))
                else: # scores[i] == scores[j]
                    pass

        return result
