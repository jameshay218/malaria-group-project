from database import *
import unittest

class TestSequenceFunctions(unittest.TestCase):
    
    def setUp(self):
        self.database = Database()
        self.successinsert = [["1888-08-08","lab","positive","test","test","0","0","id","test"],["1888-08-08","lab","negative","test","test","0","0","id","test"],["1888-08-08","lab","negative","test","test","0","0","NULL","test"]]
        
        self.failinsert = [["1888-08-08","this string has longer than thirty characters and you can't do anything about it","negative","test","test","0","0","id","test"],["1888-08-08","lab","negative","test","test","0","0","this string has longer than thirty characters and you can't do anything about it","test"],["1888-08-08","lab","negative","test","test","0","123456789100002","slideid","test"],["1888-08-08","lab","negative","test","test","12345678000000912","0","slideid","test"]]
        self.incorrectparametersinsert = [["wronglength"],["1888-08-08","lab","wrong label","test","test","0","0","id","test"],["1888-08-08","lab","positive","test","test","0","wrongzoom","id","test"],["1888-08-08","lab","positive","test","test","wrongcount","0","id","test"],["1888-08-08","lab","positive","test","test","0","0","id",";withcolon"],["1888-08-08","lab","positive","test","test","0","0",";withcolon","test"],["wrongdate","lab","positive","test","test","0","0","test","test"],["1888-08-08","withcolon;","positive","test","test","0","0","test","test"],["1888-08-08","lab","positive","withcolon;","test","0","0","test","test"]]
        
        self.successquery = [["1999-11-11;1999-11-11","NULL","NULL","NULL","NULL","0;0","0;0","NULL","NULL"],["1999-11-11;1999-11-11", "Jamestest", "positive","test","test","0;0","0;0","test","test"],["1999-11-11;1999-11-11", "Jamestest", "NULL","test","test","0;0","0;0","test","test"]]
        
        self.failquery = [["wronglength"],["1999-11-111999-11-11","NULL","NULL","NULL","NULL","0;0","0;0","NULL","NULL"],["1999-11-11;1999-11-1a", "Jamestest", "positive","test","test","0;0","0;0","test","test"],["1999-11-11;1999-11-1", "Jamestest", "positive","test","test","00","0;0","test","test"],["1999-11-11;1999-11-1", "Jamestest", "positive","test","test","0;a0","0;0","test","test"],["1999-11-11;1999-11-1", "Jamestest", "positive","test","test","0;0","00","test","test"],["1999-11-11;1999-11-1", "Jamestest", "positive","test","test","0;0","0;a0","test","test"],["1999-11-11;1999-11-11", "Jamestest", "NULL","test","test","0;0","0;0","test","test;"],["1999-11-11;1999-11-11", "Jamestest", "NULL","test","test","0;0","0;0","test;","test"],["1999-11-11;1999-11-11", "Jamestest;", "NULL","test","test","0;0","0;0","test","test"],["1999-11-11;1999-11-11", "Jamestest", "test","test","test","0;0","0;0","test","test"],["1999-11-11;1999-11-11", "Jamestest", "NULL","test;","test","0;0","0;0","test","test"],["1999-11-11;1999-11-11", "Jamestest", "NULL","test","test;","0;0","0;0","test","test"]]
    
    
    def test_insert_create_success(self):
        for i in range(0,len(self.successinsert)):
            x = self.database.insert_create(self.successinsert[i],"1")
            self.assertEqual(x, "Success")
    
    def test_insert_create_failure(self):
        for i in range(0,len(self.failinsert)):
            x = self.database.insert_create(self.failinsert[i],"1")
            self.assertEqual(x, "Something went wrong...")
    
    def test_array_check_insert_success(self):
        for i in range(0,len(self.successinsert)):
            x = self.database.array_check_insert(self.successinsert[i])
            self.assertTrue(x)
    
    def test_array_check_insert_failure(self):
        for i in range(0,len(self.incorrectparametersinsert)):
            x = self.database.array_check_insert(self.incorrectparametersinsert[i])
            self.assertFalse(x)
    
    def test_query_create_success(self):
        for i in range(0,len(self.successquery)):
            x,y = self.database.query_create(self.successquery[i])
            self.assertEqual(y, "Success")
    
    def test_query_create_failure(self):
        for i in range(0,len(self.failquery)):
            x,y = self.database.query_create(self.failquery[i])
            self.assertEqual(y, "Invalid Parameters Passed")
    
    def test_array_check_query_success(self):
        for i in range(0,len(self.successquery)):
            x = self.database.array_check_query(self.successquery[i])
            self.assertTrue(x)
    
    def test_array_check_query_failure(self):
        for i in range(0,len(self.failquery)):
            x = self.database.array_check_query(self.failquery[i])
            self.assertFalse(x)



if __name__ == '__main__':
    unittest.main()