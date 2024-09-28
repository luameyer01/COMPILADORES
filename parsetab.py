
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightFORDOWHILEIFELSERETURNrightINTPUBLICSTATICVOIDrightFLOATCHARSTRINGrightMAINOUTSYSTEMPRINTLNNleftLPARENRPARENleftLBRACERBRACEleftLBRACKETRBRACKETleftLEleftPLUSMINUSleftTIMESDIVIDErightASSIGNleftSEMICOLONCOMMAPERIODleftPLUSMINUSleftTIMESDIVIDEleftLEleftLPARENRPARENleftLBRACERBRACEleftLBRACKETRBRACKETrightASSIGNrightSTRING_LITERALASSIGN CHAR COMMA DIVIDE DO ELSE FLOAT FOR IDENTIFIER IF INT LBRACE LBRACKET LE LPAREN MAIN MINUS N NUMBER OUT PERIOD PLUS PRINTLN PUBLIC RBRACE RBRACKET RETURN RPAREN SEMICOLON STATIC STRING STRING_LITERAL SYSTEM TIMES VOID WHILEexpression : expression PLUS expression\n                | expression MINUS expression\n                | expression TIMES expression\n                | expression DIVIDE expressionexpression : NUMBERexpression : LPAREN expression RPARENexpression : IDENTIFIER ASSIGN expressionexpression : FOR\n                | DO\n                | WHILE\n                | IF\n                | ELSE\n                | RETURNexpression : expression LE expression'
    
_lr_action_items = {'NUMBER':([0,3,11,12,13,14,15,17,],[2,2,2,2,2,2,2,2,]),'LPAREN':([0,3,11,12,13,14,15,17,],[3,3,3,3,3,3,3,3,]),'IDENTIFIER':([0,3,11,12,13,14,15,17,],[4,4,4,4,4,4,4,4,]),'FOR':([0,3,11,12,13,14,15,17,],[5,5,5,5,5,5,5,5,]),'DO':([0,3,11,12,13,14,15,17,],[6,6,6,6,6,6,6,6,]),'WHILE':([0,3,11,12,13,14,15,17,],[7,7,7,7,7,7,7,7,]),'IF':([0,3,11,12,13,14,15,17,],[8,8,8,8,8,8,8,8,]),'ELSE':([0,3,11,12,13,14,15,17,],[9,9,9,9,9,9,9,9,]),'RETURN':([0,3,11,12,13,14,15,17,],[10,10,10,10,10,10,10,10,]),'$end':([1,2,5,6,7,8,9,10,18,19,20,21,22,23,24,],[0,-5,-8,-9,-10,-11,-12,-13,-1,-2,-3,-4,-14,-6,-7,]),'PLUS':([1,2,5,6,7,8,9,10,16,18,19,20,21,22,23,24,],[11,-5,-8,-9,-10,-11,-12,-13,11,-1,-2,-3,-4,11,-6,-7,]),'MINUS':([1,2,5,6,7,8,9,10,16,18,19,20,21,22,23,24,],[12,-5,-8,-9,-10,-11,-12,-13,12,-1,-2,-3,-4,12,-6,-7,]),'TIMES':([1,2,5,6,7,8,9,10,16,18,19,20,21,22,23,24,],[13,-5,-8,-9,-10,-11,-12,-13,13,13,13,-3,-4,13,-6,-7,]),'DIVIDE':([1,2,5,6,7,8,9,10,16,18,19,20,21,22,23,24,],[14,-5,-8,-9,-10,-11,-12,-13,14,14,14,-3,-4,14,-6,-7,]),'LE':([1,2,5,6,7,8,9,10,16,18,19,20,21,22,23,24,],[15,-5,-8,-9,-10,-11,-12,-13,15,-1,-2,-3,-4,-14,-6,-7,]),'RPAREN':([2,5,6,7,8,9,10,16,18,19,20,21,22,23,24,],[-5,-8,-9,-10,-11,-12,-13,23,-1,-2,-3,-4,-14,-6,-7,]),'ASSIGN':([4,],[17,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,3,11,12,13,14,15,17,],[1,16,18,19,20,21,22,24,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','app.py',35),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','app.py',36),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','app.py',37),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','app.py',38),
  ('expression -> NUMBER','expression',1,'p_expression_number','app.py',50),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_parentheses','app.py',55),
  ('expression -> IDENTIFIER ASSIGN expression','expression',3,'p_expression_assign','app.py',60),
  ('expression -> FOR','expression',1,'p_expression_reserved','app.py',65),
  ('expression -> DO','expression',1,'p_expression_reserved','app.py',66),
  ('expression -> WHILE','expression',1,'p_expression_reserved','app.py',67),
  ('expression -> IF','expression',1,'p_expression_reserved','app.py',68),
  ('expression -> ELSE','expression',1,'p_expression_reserved','app.py',69),
  ('expression -> RETURN','expression',1,'p_expression_reserved','app.py',70),
  ('expression -> expression LE expression','expression',3,'p_expression_comparison','app.py',75),
]
