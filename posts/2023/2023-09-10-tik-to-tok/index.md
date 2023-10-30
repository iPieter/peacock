The resume is one of the jobseekers' first chances of making a good impression on organisations. Recruiters usually spend less than a minute to screen an application, so if key information is missing, a candidate might not be invited to a job interview.

Many websites offer guides on how to write a resume, however, standards and expected formats differ across industries and countries. Jobseekers can learn about resume writing in courses offered by e.g. career center services at universities or Public Employment services, but while these courses offer valuable information, not all groups of jobseekers have access to these services. Consequently, they miss out on general advice on the structure and layout of resumes, but more importantly also on tailored advice, such as which sections of a resume are essential in a specific field or which skills could be added based on the job they are applying for. 

Existing tools differ in functionality. For instance, on LinkedIn, the resume is generated automatically from the information the user input on their LinkedIn profile. EuroPass lets users input information and generates a resume based on a selected template. Novorésumé also lets users input their information and choose a template, and their tool gives additional information on the different sections. Unlike existing tools, our tool gives advice based on either the job title a user inputs or on a specific vacancy.

We analysed the occurrence and order of section titles in a dataset of 444k resumes that were collected by VDAB, the Flemish public employment service in Belgium. A typical resume consists of different sections, such as work experience and education, which the jobseeker can order depending on their preference and which aspects they want to highlight. Some sections are also dependent on the sector the jobseeker aims for. The most common sections are work experience and education, which are in virtually all resumes. Some sections are not common at all, for instance, only 5 out of 444k resumes included a "personal objective" section. We also found that some jobseekers provided information which might harm their chances of being invited to job interviews, such as a section called "negative personality traits" with traits like "too focused on work". 

Our co-creative tool ResumeTailor uses two methods we developed to assist users when writing a resume. Firstly, we use an autoregressive model to generate example resumes or resume outlines based on the target job that a user provides. This model can help jobseekers that do not have a resume to start from, such as students who will enter the job market. Secondly, we create a domain-adapted language model to provide contextual suggestions when editing a resume, such as relevant, but missing skills.


![resume-writer.png](resume-writer.png)


We focus on the writing aspect and content of a resume. The layout and style choices (font, colors, ...) are beyond the scope of this paper. Instead, ResumeTailor helps users with the actual content of their resume.

## Generating Resume Outlines 
We first asked the user to provide their name and target job. We prompt GPT-3 to generate resume outlines and example resumes based on this information. We argue that personalised templates based on the user's input and target job are more helpful than pre-defined templates.

## Contexual Suggesions with Language Models
To provide the user with suggestions, we created a domain-adapted language model, which we call ResumeRobBERT, that we trained on the aforementioned dataset of 444k Dutch resumes from Flanders using the Dutch language model RobBERT as the base model. This model interacts with the user by giving suggestions based on the surrounding context of the user's cursor position, e.g. to suggest missing skills.