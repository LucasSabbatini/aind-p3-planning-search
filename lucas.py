"""
In this script, I'll redefine classes and unctions for the purpose of studiyng and understanding them
this is not a helper script
"""



# from aima.planning.py
class Action:
	"""
	Defines an action schema usig preconsitions and effects
	"""

	def __init__(self, action, precond, effect):
		"""
		Arguments
		---------
		action : Expr object with the action logical statement
		precond : [preconditions_pos, preconditions_neg], where
			preconditions_pos is a list of positive preconditions (expr objects)
			preconditions_neg ia a list of negative preconditions (expr objects)
			so that the action may be taken

		effect : [effect_add, effect_rem], where
			effect_add : logical literals to be added to the positive list of the state
			effect_rem : logical statements to be removed from the positive list
		WE ARE WORKING WITH FULL DESCRIPTIONS OF THE STATE, SO WE HAVE BOTH WHAT 
		IS POSITIVE AND WHAT IS NEGATIVE.
		!!! so far I don't know what happens with the negative. It is to expect 
		that positive items removed from the positive list may be added to the
		negative list.
		"""
		self.name = action.op
		self.args = action.args
		self.precond_pos = precond[0]
		self.precond_neg = precond[1]
		self.effect_add = effect[0]
		self.effect_rem = effect[1]

	def __call__(self, kb, args):
		return self.act(kb, args)

	def act(self, kb, args):
		if not self,check_precond(kb, args):
			raise Exception("Action pre-conditions not satisfied")
		for clause in self.effect_rem:
			kb.retract(self.substitute(clause, args))
		for clause in self.effects_add:
			kb.tell(self.substitute(clause, args))

	def check_precond(self, kb ,args):
		# checks if a positive precondition is not in the kb clauses
		for clause in self.precond_pos:
			if self.substitute(clause, args) not in kb.clauses:
				return False
		# checks if a negative precondition is in the knowledge-base clauses
		for clause in self.precond_neg:
			if self.substitute(clause, args) in kb.clauses:
				return False


	def substitute(self, e, args):
		new_args = list(e.args)
		for num, x, in enumerate(e.args):
			for i in range(len(self.args)):
				if self.args[i] == x:
					new_args[num] = args[i]
		return Expr(e.op, *new_args)


# from utils.py
def expr(x):
	if isinstance(x, str):
		return eval(expr_handle_infix_ops(x), defaultkeydict(Symbol))
	else:
		return x


# my_air_cargo_problems.py

class AirCargoProblem(Problem):

	def __init__(self, cargos, planes, airports, initial: FluentState, goal: list):
		self.state_map = initial.pos + initial.neg
		self.initial_state_TF = encode_state(initial, self.state_map)
		# initalizing problem object with encoded initial state and goal
		Problem.__init__(saelf, self.initia_state_TF, goal=goal)
		self.cargos = cargos
		self.planes = planes
		self.airports = airports
		self.actions_list = self.get_actions()


	def load_actions():
		loads = []

		for cargo in self.cargos:
			for airplane in self.airplanes:
				for airport in self.airports:
					# action is created as follows:
					# Action(expr())
					action_expr = expr(str("Load"))

	def h_ignore_preconditions(self, node: Node):
		"""
		This s the heuristic to be implemented.
		since this is a planning search problem, states are not representented in an 
		atomic manner, but in a factored one. This means that there can be deduced general
		heuristics (domain independent heuristics) for this problem

		This heuristic in particular will estimte the number of actions required
		to get from current state to a state that satisfies all of the goal conditions
		(GOAL IS NOT A SPECIFIC STATE, IT IS A SET OF CONDITIONS THAT MUST BE MET, so 
		there are more then one possible state)

		node : Node object:
			has four attributes: state, parent, action, path_cost and depth


		goal state is going to have some conditions, the objective is to satisfy them,
		starting at the current state. This heuristic only counts the number of actions needed
		to satisfy these conditions, not considering the pre-conditions to take actions

		What we need then is the number of unsatisfied conditions of current state
		and then find the number of actions that would take there

		Current state is codified by the node.state attribute. There are two possibilities
		for the codification of the sate: string or a FluentState object
			If state is a tring, we need the decode_stae fuction to retrieve a FluentState
		pobject with the positive and negative fluents

		"""

		# AirCargoProblem objet has six attributes:
		#	state_map, intial_state_Tf, cargos, planes, airports, action_list
		# AirCargoProblem.actions return only possible actions

		# Ignore precoditions to take actions
		actions_taken = []
		actions_effects = []

		# number of conditions on goal satte that are not met in current
		fluents_remaining = 0
		for fluent in self.goal:
			# if a fluent in the goal state is not in current, append to the list
			if fluent not in node.state.pos:
				fluets_remaining += 1


		count = 0
		for action in self.actions_list:
			valid = False
			for effect in action.effect_add: 
			# iterating over fluents that become positive when the action is applied
				# effect must be a goal condition and not be already in urrent state
				if effect in self.goal and effect not in node.state.pos:
					valid = True
					actions_effects.append(effect)
			if valid:
				count += 1
				actions_taken.append(action)
		for fluent in self.goal:
			if fluent not in actions_effects:
				raise Exception('There\'s a condition not met. Planning is impossible.')

		return count


# ----------------------------------------------------------------------------------
# GRAPHPLAN algorithm

def graphplan(problem):
	"""
	Graph plan algorithm
	"""
	graph = initial_planning_graph(problem) # extract the initia graph from the problem
	goals = conjuncts(problem.goal) # return the conjunction of literals of goal state
	nogoods = empty_hashtable # don't know what this is yet

	for tl in range(0, "inf"):
		#terminal test
		if non_mutex(goals, graph.state):
			solution = return_solution(graph, goals, graph.num_levels, nogoods)
			if not failure(solution):
		if has_leveled_off(graph, graph) and has_leveled_off(nogoods, graph):
			return False

		graph = expand_graph(graph, problem)
		# Adds action with existing preconditions to A level along with persintence
		# actions for state literals, and adds the effects of actions into the next
		# state level

def expand_graph(graph, problem):







    def competing_needs_mutex(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:
        """
        Test a pair of actions for mutual exclusion, returning True if one of
        the precondition of one action is mutex with a precondition of the
        other action.

        :param node_a1: PgNode_a
        :param node_a2: PgNode_a
        :return: bool
        """
        # print("Actions 1 and 2: ", node_a1.action, node_a2.action)
        # print("Node 1: ", node_a1.action.precond_pos, ", ", node_a2.action.precond_neg)
        # print("Node 2: ", node_a2.action.precond_pos, ", ", node_a1.action.precond_neg)


        """
        !!!!!!!! TO CHANGE !!!!!!!!!
        Maybe instead of using preconditions from the sub object action I should look
        at the parents of these nodes, and check their comp
        """


        # iterating over parents of actions, which are PgNode_s objects.

        for parent1 in node_a1.parents:
        	
            for parent2 in node_s2.parents:
				print("type parent1: ", type(parent1))
				print("type parent2: ", type(parent2))
                if parent1.is_mutex(parent2):
                    return True

        return False


        # for precon in node_a1.action.precond_pos:
        #     if precon in node_a2.action.precond_neg:
        #         return True

        # for precon in node_a2.action.precond_pos:
        #     if precon in node_a1.action.precond_neg:
        #         return True
        # return False

        # for precon in node_a1.parents










		