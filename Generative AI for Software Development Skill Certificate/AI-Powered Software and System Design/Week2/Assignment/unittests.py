import numpy as np
from dlai_grader.grading import test_case, print_feedback
from types import FunctionType
from dlai_grader.io import suppress_stdout_stderr
import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import pandas as pd

# Creates the database for the social network

def create_database_unittest():
    Base = declarative_base()

    friendships = Table('friendships', Base.metadata,
                        Column('person_id', Integer, ForeignKey('people.id'), primary_key=True),
                        Column('friend_id', Integer, ForeignKey('people.id'), primary_key=True))

    club_members = Table('club_members', Base.metadata,
                         Column('person_id', Integer, ForeignKey('people.id'), primary_key=True),
                         Column('club_id', Integer, ForeignKey('clubs.id'), primary_key=True))

    class Person(Base):
        __tablename__ = 'people'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        age = Column(Integer)
        gender = Column(String)
        location = Column(String)
        friends = relationship("Person",
                               secondary=friendships,
                               primaryjoin=id == friendships.c.person_id,
                               secondaryjoin=id == friendships.c.friend_id)
        clubs = relationship("Club", secondary=club_members, back_populates="members")

    class Club(Base):
        __tablename__ = 'clubs'
        id = Column(Integer, primary_key=True)
        description = Column(String)
        members = relationship("Person", secondary=club_members, back_populates="clubs")

    if os.path.exists("/tmp/social_network.db"):
        os.remove("/tmp/social_network.db")
    engine = create_engine(f'sqlite:////tmp/"social_network.db"', echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session, Club, Person, friendships, club_members


def test_load_data_from_csv(function):
    def g():
        function_name = function.__name__
        cases = []

        df = pd.read_csv("members.csv", converters = {'Friendships':eval, "Clubs": eval})
        # Check if function is a function method exists
        t = test_case()
        if not isinstance(function, FunctionType):
            t.failed = True
            t.msg = f"{function_name} is not a function"
            t.want = f"{function_name} must be a function"
            t.got = f"Type of {function_name} is {type(function_name)}"
            return [t]
        if 'tmp' not in os.listdir("/"):
            os.mkdir('/tmp')
        # List all files in the directory
        for filename in os.listdir('/tmp'):
            # Create the full file path
            file_path = os.path.join('/tmp', filename)
            # Check if it is a file (and not a directory/subdirectory)
            if os.path.isfile(file_path):
                # Delete the file silently
                os.remove(file_path)
        with suppress_stdout_stderr():
            session, Club, Person, friendships, club_members = create_database_unittest()
        function(session, Club, Person, friendships, club_members, csv_path="members.csv")
        persons = session.query(Person).all()
        t = test_case()
        if len(persons) != len(df):
            t.failed = True
            t.msg = "Incorrect number of persons in the database"
            t.want = len(df)
            t.got = len(persons)
            return [t]
        names = ['John Rocha',
 'William Ruiz',
 'Jackie Mccullough',
 'Michael Powell',
 'Scott Boyd',
 'Andrew Williams',
 'Amanda Norris',
 'Becky Peterson',
 'Julie Hutchinson',
 'Mark Allen',
 'Nicholas Harrington',
 'Michael Clark',
 'Christina Murphy',
 'Omar Mason',
 'Luis Kim',
 'Brian Mays',
 'Eric Dougherty',
 'Nathan Mendez',
 'Elizabeth Hernandez',
 'Mark Mcintyre']
        learner_names = [x.name for x in persons]
        names.sort()
        learner_names.sort()
        t = test_case()
        if list(names) != learner_names:
            t.failed = True
            t.msg = "Incorrect persons in dataset"
            t.want = f"Set of persons: {names}"
            t.got = f"Set of persons: {learner_names}"
            return [t]
        query = session.query(Person.name, Person.location, Person.gender, Person.age)
        persons_list = query.all()
        t = test_case()
        for person in persons_list:
            if not isinstance(person[-1], int):
                t.failed = True
                t.msg = "Incorrect type for persons age"
                t.want = "Integer"
                t.got = type(person[-1])
                cases.append(t)
                return [t]
        persons_data = np.array([[df.loc[i,'Name'] + ' ' + df.loc[i,'Surname'], df.loc[i,'Location'], df.loc[i, 'Gender'], df.loc[i, 'Age']] for i in range(len(df))])
        persons_list = np.array(persons_list)
        persons_list.sort(axis = 0)
        persons_data.sort(axis = 0)
        for person_learner, person_solution in zip(persons_list, persons_data):
            name_learner,location_learner,gender_learner,age_learner = person_learner
            name_solution,location_solution,gender_solution,age_solution = person_solution
            t = test_case()
            if location_learner != location_solution:
                t.failed = True
                t.msg = f"Incorrect location for person {name_solution}"
                t.want = f"{location_solution}"
                t.got = f"{location_learner}"
            cases.append(t)
            t = test_case()
            if gender_learner != gender_solution:
                t.failed = True
                t.msg = f"Incorrect gender for person {name_solution}"
                t.want = f"{gender_solution}"
                t.got = f"{gender_learner}"
            cases.append(t)
            if age_learner != age_solution:
                t.failed = True
                t.msg = f"Incorrect age for person {name_solution}"
                t.want = f"{age_solution}"
                t.got = f"{age_learner}"
            cases.append(t)
        return cases
    cases = g()
    print_feedback(cases)


def test_get_club_members(load_data_from_csv, function):
    
    correct = {'Fitness Club': ['John Rocha',
  'Amanda Norris',
  'Michael Clark',
  'Christina Murphy'],
 'Travel Club': ['William Ruiz',
  'Michael Powell',
  'Becky Peterson',
  'Nicholas Harrington',
  'Luis Kim',
  'Nathan Mendez'],
 'Art Club': ['William Ruiz',
  'Jackie Mccullough',
  'Amanda Norris',
  'Becky Peterson',
  'Mark Allen',
  'Brian Mays',
  'Eric Dougherty',
  'Nathan Mendez'],
 'Cooking Club': ['William Ruiz', 'Brian Mays', 'Eric Dougherty'],
 'Hiking Club': ['Jackie Mccullough',
  'Michael Powell',
  'Amanda Norris',
  'Michael Clark',
  'Christina Murphy',
  'Luis Kim',
  'Nathan Mendez'],
 'Chess Club': ['Michael Powell',
  'Andrew Williams',
  'Michael Clark',
  'Christina Murphy',
  'Eric Dougherty',
  'Elizabeth Hernandez'],
 'Gaming Club': ['Michael Powell',
  'Scott Boyd',
  'Julie Hutchinson',
  'Omar Mason',
  'Elizabeth Hernandez',
  'Mark Mcintyre'],
 'Book Club': ['Michael Powell',
  'Amanda Norris',
  'Nicholas Harrington',
  'Brian Mays',
  'Elizabeth Hernandez',
  'Mark Mcintyre'],
 'Photography Club': ['Amanda Norris', 'Christina Murphy', 'Brian Mays'],
 'Music Club': ['Julie Hutchinson',
  'Mark Allen',
  'Luis Kim',
  'Nathan Mendez',
  'Elizabeth Hernandez']}
    def g():
        function_name = function.__name__
        cases = []

        df = pd.read_csv("members.csv", converters = {'Friendships':eval, "Clubs": eval})
        # Check if function is a function method exists
        t = test_case()
        if not isinstance(function, FunctionType):
            t.failed = True
            t.msg = f"{function_name} is not a function"
            t.want = f"{function_name} must be a function"
            t.got = f"Type of {function_name} is {type(function_name)}"
            return [t]
        if 'tmp' not in os.listdir("/"):
            os.mkdir('/tmp')
        # List all files in the directory
        for filename in os.listdir('/tmp'):
            # Create the full file path
            file_path = os.path.join('/tmp', filename)
            # Check if it is a file (and not a directory/subdirectory)
            if os.path.isfile(file_path):
                # Delete the file silently
                os.remove(file_path)
        with suppress_stdout_stderr():
            session, Club, Person, friendships, club_members = create_database_unittest()
        load_data_from_csv(session, Club, Person, friendships, club_members, csv_path="members.csv")
        learner = {}
        for c in correct.keys():
            t = test_case()
            try:
                members = [x.name for x in function(session, c)]
                learner[c] = members
            except Exception as e:
                t.failed = True
                t.msg = f"Failed execution for club description {c}"
                t.want = "Function must run properly"
                t.got = f"Exception thrown: {e}"
                return [t]
            
        for c in correct.keys():
            t = test_case()
            learner_list = learner[c]
            solution_list = correct[c]
            learner_list.sort()
            solution_list.sort()
            if learner_list != solution_list:
                t.failed = True
                t.msg = f"Incorrect club members for club description {c}"
                t.want = f"{solution_list}"
                t.got = f"{learner_list}"
            cases.append(t)
        session.close()
        return cases
    cases = g()
    print_feedback(cases)

def test_get_friends_of_person(load_data_from_csv, function):
    
    def g():
        function_name = function.__name__
        cases = []

        df = pd.read_csv("members.csv", converters = {'Friendships':eval, "Clubs": eval})
        # Check if function is a function method exists
        t = test_case()
        if not isinstance(function, FunctionType):
            t.failed = True
            t.msg = f"{function_name} is not a function"
            t.want = f"{function_name} must be a function"
            t.got = f"Type of {function_name} is {type(function_name)}"
            return [t]
        if 'tmp' not in os.listdir("/"):
            os.mkdir('/tmp')
        # List all files in the directory
        for filename in os.listdir('/tmp'):
            # Create the full file path
            file_path = os.path.join('/tmp', filename)
            # Check if it is a file (and not a directory/subdirectory)
            if os.path.isfile(file_path):
                # Delete the file silently
                os.remove(file_path)
        with suppress_stdout_stderr():
            session, Club, Person, friendships, club_members = create_database_unittest()
        load_data_from_csv(session, Club, Person, friendships, club_members, csv_path="members.csv")
        learner = {}
        correct = {'John Rocha': ['Scott Boyd',
  'Andrew Williams',
  'Nicholas Harrington',
  'Christina Murphy',
  'Luis Kim',
  'Mark Mcintyre'],
 'William Ruiz': ['Michael Powell',
  'Mark Allen',
  'Nicholas Harrington',
  'Brian Mays',
  'Nathan Mendez'],
 'Jackie Mccullough': ['Scott Boyd',
  'Amanda Norris',
  'Mark Allen',
  'Nicholas Harrington'],
 'Michael Powell': ['Jackie Mccullough',
  'Amanda Norris',
  'Becky Peterson',
  'Michael Clark',
  'Omar Mason',
  'Luis Kim'],
 'Scott Boyd': ['John Rocha',
  'William Ruiz',
  'Andrew Williams',
  'Nicholas Harrington',
  'Michael Clark',
  'Brian Mays',
  'Nathan Mendez'],
 'Andrew Williams': ['William Ruiz',
  'Jackie Mccullough',
  'Michael Powell',
  'Scott Boyd',
  'Becky Peterson',
  'Julie Hutchinson',
  'Michael Clark'],
 'Amanda Norris': ['Mark Allen', 'Nicholas Harrington', 'Elizabeth Hernandez'],
 'Becky Peterson': ['William Ruiz', 'Amanda Norris', 'Michael Clark'],
 'Julie Hutchinson': ['Jackie Mccullough',
  'Scott Boyd',
  'Andrew Williams',
  'Omar Mason',
  'Brian Mays',
  'Eric Dougherty'],
 'Mark Allen': ['Jackie Mccullough',
  'Scott Boyd',
  'Andrew Williams',
  'Becky Peterson',
  'Nicholas Harrington',
  'Michael Clark',
  'Christina Murphy',
  'Eric Dougherty'],
 'Nicholas Harrington': ['William Ruiz',
  'Scott Boyd',
  'Andrew Williams',
  'Brian Mays',
  'Elizabeth Hernandez'],
 'Michael Clark': ['William Ruiz',
  'Scott Boyd',
  'Nicholas Harrington',
  'Brian Mays',
  'Eric Dougherty',
  'Mark Mcintyre'],
 'Christina Murphy': ['John Rocha',
  'Michael Powell',
  'Julie Hutchinson',
  'Nicholas Harrington',
  'Omar Mason',
  'Luis Kim',
  'Brian Mays',
  'Eric Dougherty',
  'Nathan Mendez'],
 'Omar Mason': ['Jackie Mccullough',
  'Mark Allen',
  'Nicholas Harrington',
  'Christina Murphy',
  'Luis Kim',
  'Nathan Mendez',
  'Mark Mcintyre'],
 'Luis Kim': ['William Ruiz', 'Mark Allen', 'Nathan Mendez'],
 'Brian Mays': ['John Rocha',
  'Michael Powell',
  'Andrew Williams',
  'Amanda Norris',
  'Julie Hutchinson',
  'Michael Clark',
  'Omar Mason'],
 'Eric Dougherty': ['Scott Boyd',
  'Andrew Williams',
  'Amanda Norris',
  'Julie Hutchinson'],
 'Nathan Mendez': ['John Rocha',
  'William Ruiz',
  'Scott Boyd',
  'Andrew Williams',
  'Luis Kim',
  'Elizabeth Hernandez'],
 'Elizabeth Hernandez': ['Jackie Mccullough',
  'Michael Powell',
  'Becky Peterson',
  'Christina Murphy',
  'Luis Kim',
  'Brian Mays',
  'Eric Dougherty'],
 'Mark Mcintyre': ['William Ruiz',
  'Andrew Williams',
  'Mark Allen',
  'Nicholas Harrington',
  'Omar Mason',
  'Elizabeth Hernandez']}
        for c in correct.keys():
            t = test_case()
            try:
                members = [x.name for x in function(session, c)]
                learner[c] = members
            except Exception as e:
                t.failed = True
                t.msg = f"Failed execution for club description {c}"
                t.want = "Function must run properly"
                t.got = f"Exception thrown: {e}"
                return [t]
            
        for c in correct.keys():
            t = test_case()
            learner_list = learner[c]
            solution_list = correct[c]
            learner_list.sort()
            solution_list.sort()
            if learner_list != solution_list:
                t.failed = True
                t.msg = f"Incorrect friends for person {c}"
                t.want = f"{solution_list}"
                t.got = f"{learner_list}"
            cases.append(t)
        return cases
    cases = g()
    print_feedback(cases)
            
def test_get_persons_who_consider_them_friend(load_data_from_csv, function):
    
    correct = {'John Rocha': ['Scott Boyd',
  'Christina Murphy',
  'Brian Mays',
  'Nathan Mendez'],
 'William Ruiz': ['Scott Boyd',
  'Andrew Williams',
  'Becky Peterson',
  'Nicholas Harrington',
  'Michael Clark',
  'Luis Kim',
  'Nathan Mendez',
  'Mark Mcintyre'],
 'Jackie Mccullough': ['Michael Powell',
  'Andrew Williams',
  'Julie Hutchinson',
  'Mark Allen',
  'Omar Mason',
  'Elizabeth Hernandez'],
 'Michael Powell': ['William Ruiz',
  'Andrew Williams',
  'Christina Murphy',
  'Brian Mays',
  'Elizabeth Hernandez'],
 'Scott Boyd': ['John Rocha',
  'Jackie Mccullough',
  'Andrew Williams',
  'Julie Hutchinson',
  'Mark Allen',
  'Nicholas Harrington',
  'Michael Clark',
  'Eric Dougherty',
  'Nathan Mendez'],
 'Andrew Williams': ['John Rocha',
  'Scott Boyd',
  'Julie Hutchinson',
  'Mark Allen',
  'Nicholas Harrington',
  'Brian Mays',
  'Eric Dougherty',
  'Nathan Mendez',
  'Mark Mcintyre'],
 'Amanda Norris': ['Jackie Mccullough',
  'Michael Powell',
  'Becky Peterson',
  'Brian Mays',
  'Eric Dougherty'],
 'Becky Peterson': ['Michael Powell',
  'Andrew Williams',
  'Mark Allen',
  'Elizabeth Hernandez'],
 'Julie Hutchinson': ['Andrew Williams',
  'Christina Murphy',
  'Brian Mays',
  'Eric Dougherty'],
 'Mark Allen': ['William Ruiz',
  'Jackie Mccullough',
  'Amanda Norris',
  'Omar Mason',
  'Luis Kim',
  'Mark Mcintyre'],
 'Nicholas Harrington': ['John Rocha',
  'William Ruiz',
  'Jackie Mccullough',
  'Scott Boyd',
  'Amanda Norris',
  'Mark Allen',
  'Michael Clark',
  'Christina Murphy',
  'Omar Mason',
  'Mark Mcintyre'],
 'Michael Clark': ['Michael Powell',
  'Scott Boyd',
  'Andrew Williams',
  'Becky Peterson',
  'Mark Allen',
  'Brian Mays'],
 'Christina Murphy': ['John Rocha',
  'Mark Allen',
  'Omar Mason',
  'Elizabeth Hernandez'],
 'Omar Mason': ['Michael Powell',
  'Julie Hutchinson',
  'Christina Murphy',
  'Brian Mays',
  'Mark Mcintyre'],
 'Luis Kim': ['John Rocha',
  'Michael Powell',
  'Christina Murphy',
  'Omar Mason',
  'Nathan Mendez',
  'Elizabeth Hernandez'],
 'Brian Mays': ['William Ruiz',
  'Scott Boyd',
  'Julie Hutchinson',
  'Nicholas Harrington',
  'Michael Clark',
  'Christina Murphy',
  'Elizabeth Hernandez'],
 'Eric Dougherty': ['Julie Hutchinson',
  'Mark Allen',
  'Michael Clark',
  'Christina Murphy',
  'Elizabeth Hernandez'],
 'Nathan Mendez': ['William Ruiz',
  'Scott Boyd',
  'Christina Murphy',
  'Omar Mason',
  'Luis Kim'],
 'Elizabeth Hernandez': ['Amanda Norris',
  'Nicholas Harrington',
  'Nathan Mendez',
  'Mark Mcintyre'],
 'Mark Mcintyre': ['John Rocha', 'Michael Clark', 'Omar Mason']}
    def g():
        function_name = function.__name__
        cases = []

        df = pd.read_csv("members.csv", converters = {'Friendships':eval, "Clubs": eval})
        # Check if function is a function method exists
        t = test_case()
        if not isinstance(function, FunctionType):
            t.failed = True
            t.msg = f"{function_name} is not a function"
            t.want = f"{function_name} must be a function"
            t.got = f"Type of {function_name} is {type(function_name)}"
            return [t]
        if 'tmp' not in os.listdir("/"):
            os.mkdir('/tmp')
        # List all files in the directory
        for filename in os.listdir('/tmp'):
            # Create the full file path
            file_path = os.path.join('/tmp', filename)
            # Check if it is a file (and not a directory/subdirectory)
            if os.path.isfile(file_path):
                # Delete the file silently
                os.remove(file_path)
        with suppress_stdout_stderr():
            session, Club, Person, friendships, club_members = create_database_unittest()
        load_data_from_csv(session, Club, Person, friendships, club_members, csv_path="members.csv")
        learner = {}
        for c in correct:
            t = test_case()
            try:
                members = [x.name for x in function(session, c)]
                learner[c] = members
            except Exception as e:
                t.failed = True
                t.msg = f"Failed execution for club description {c}"
                t.want = "Function must run properly"
                t.got = f"Exception thrown: {e}"
                return [t]
            
        for i,c in enumerate(correct):
            t = test_case()
            learner_list = learner[c]
            solution_name = correct[c]

            if len(set(learner_list)) != len(learner_list):
                t.failed = True
                t.msg = f"There are duplicate friends in member {c} friends list"
                t.want = f"Friends list must have unique values"
                t.got = f"Friends list of {c} has at least one duplicate value"
            cases.append(t)

            t = test_case()
            if c in learner_list:
                t.failed = True
                t.msg = f"{c} is contained in its friends list"
                t.want = f"A member cannot be a friend of itself"
                t.got = f"Friends list of {c} contains {c}"
            cases.append(t)
            for c in correct.keys():
                t = test_case()
                learner_list = learner[c]
                solution_list = correct[c]
                learner_list.sort()
                solution_list.sort()
                if learner_list != solution_list:
                    t.failed = True
                    t.msg = f"Incorrect persons that person {c} consider as friends."
                    t.want = f"{solution_list}"
                    t.got = f"{learner_list}"
                cases.append(t)

        return cases
    cases = g()
    print_feedback(cases)
                      
    
        
    