import unittest
from types import SimpleNamespace
from career_life import best_assets
class BestAssetsTests(unittest.TestCase):
 def test_best_in_each_category_is_independent_of_order_and_quantity(self):
  c=SimpleNamespace(life={'owned':{'designer':1,'supercar':1,'mansion':1,'studio':1,'utility':1000,'casual':1}})
  self.assertEqual({k:v[0] for k,v in best_assets(c).items()},{'home':'mansion','car':'supercar','clothes':'designer'})
 def test_mixed_categories_do_not_invent_unpurchased_upgrades(self):
  c=SimpleNamespace(life={'owned':{'studio':1,'utility':1,'designer':1,'handbag':100}})
  self.assertEqual({k:v[0] for k,v in best_assets(c).items()},{'home':'studio','car':'utility','clothes':'designer'})
 def test_no_purchases_returns_no_owned_assets(self):
  self.assertEqual(best_assets(SimpleNamespace(life={'owned':{}})),{'home':None,'car':None,'clothes':None})
