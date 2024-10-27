from openai import OpenAI
client = OpenAI()

def initialQuiz(student):

    quizLength = 5

    initial_prompt = f"You are a math aptitude assessment software. Given that the age of the student is {student.age}, " "create the first question of a math aptitude test. The aptitude test will assess math skills with the intent " "of creating a 'learningBio' that I will give back to you in the future to help you create lesson plans for the student. " "The question should only be a math question written in latex formatting with 5 choices for answers, formatted as: \n" "#) Question:\nA) (Possible Answer a)\nB) (Possible Answer b)\nC) (Possible Answer c)\nD) (Possible Answer d)\nE) None of the Above The answer that will be given will just be a letter, A, B, C, D, or E." 

    currentQuiz = ""

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": initial_prompt}
        ]
    )

    response = completion.choices[0].message.content
    print(response)

    answer = input("Answer: ")

    currentQuiz += f"<question>{response}</question><answer>{answer}</answer>"

    for i in range(quizLength - 1):

        recurringPrompt = f"You are a math aptitude assessment software. Given that the age of the student is {student.age} and the questions and answers " f"from the student so far are: \n{currentQuiz}\n, where the questions begin with <question> and ends <\question> and the corresponding answer after each question begins with  <answer> and ends with <\answer>. generate the next question for the aptitude test. " "The next question should not match any previous questions, and if previous answers were wrong, that should be considered in order " "to find where the student is at in terms of their mathematical capabilities. " "The question should only be a math question written in latex formatting with 5 choices for answers, formatted as: " "1) Question:\nA) (Possible Answer a)\nB) (Possible Answer b)\nC) (Possible Answer c)\nD) (Possible Answer d)\nE) None of the Above The answer that will be given will just be a letter, A, B, C, D, or E."

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": recurringPrompt}
            ]
        )

        response = completion.choices[0].message.content
        print(response)

        answer = input("Answer: ")

        currentQuiz += f"<question>{response}</question><answer>{answer}</answer>"
        
    finalBioPrompt =  f"You are a math aptitude assessment software. A student has taken the following test with the following questions and answers: {currentQuiz}. Notice that each question begins with <question> and ends with </question>, and the answer that immediately follows it begins with <answer> and ends with </answer>. " "The aptitude test assessed math skills with the intent of creating a 'learningBio' that can be used in the future to create assignments " "and lesson plans. Give me the learningBio based on the test and answers of the student that have been provided. " "Give very specific detail in this bio, covering every topic that the test covered, as well as topics that would be good to review, " "and topics that should be learned next that weren’t tested on."

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": finalBioPrompt}
        ]
    )

    response = completion.choices[0].message.content
    
    finalAssignment = ( "You are an assignment generator. You are given the following bio about a student that has recently taken a " "math aptitude test. Based on the bio you will create an assignment that will be long enough to help the student " "learn the next topic they need to learn to progress their knowledge of mathematics. The output will be a fully formatted latex text file. ONLY RETURN A VALID LATEX FILE, NOTHING ELSE. Here is the given bio: " + response )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": finalAssignment}
        ]
    )

    response = completion.choices[0].message.content
    
    with open("assignment.tex", "w") as file:
        file.write(response.replace("```latex", "").replace("```", ""))

class Student:
    def __init__(self, ID: str, firstName: str, lastName: str, age: int, userName: str, password: str):
        self.ID = ID
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.userName = userName
        self.password = password
        self.learningBio = ""  # Initially empty, will be filled by generateBioWithEntryQuiz

student = Student( ID="12345", firstName="John", lastName="Doe", age=11, userName="johndoe16", password="securePassword123" )

initialQuiz(student)