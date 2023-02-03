## Why Bother Building a RAP?

Before we go through how to set everything up we should probably explain why we are going to all this effort. The answer is to achieve a RAP.

Reproducible Analytics Pipelines (RAPs) are what everyone should be using for any research data project - see: https://nhsengland.github.io/nhs-r-reporting/tutorials/rap.html. However this is difficult to achieve. Particularly in a federated project like this.

If you put non-standarised inputs into a project like this then you get non-standardised outputs and typically the workload for analysts is multiplied. A RAP solves that problem.

## Why Python?

There are really only two viable options to achieve a RAP in a decentralised manner - R and Python (both combined with SQL in the backend).

R is fab and contains many extremely powerful statistical packages and tidyverse for assembling data but it has some significant drawbacks - the biggest one being its smaller community leading to a more limited range of use-cases for the language. Python has significant drawbacks (like slow computation vs other languages like C++) but it has 3 major advantages which have enabled it to thrive:

1. It is extremely easy to read and learn vs other languages.
2. You can do almost anything with it (It is a true penknife lanugage).
3. It has enormous machine learning and AI support.

You can make an alternative case for R and some sites do use R for their research data engineering but we have gone with python here. If you would like to copy this pipeline and make an R version go for it - as long as the validation steps match it should work just as well.

## Starting out

It is daunting starting out with a new language but the best way to learn is just to start using it. We recommend you use minicondas as it is free of licensing restrictions and is simple to set up. Please go to [Minicondas Installers](https://docs.conda.io/en/latest/miniconda.html) and download the appropriate distribution of it.

I have run through this installation from start to scratch multiple times and it should work providing access is unblocked. If it doesn't please get in contact.

## But my Trust/University is Blocking me from installing it

This is a common problem. Fortunately it is one easy to overcome if you know how. Firstly try installing it as an administrator but this will probably not work as it is probably being blocked by an insitutional policy / antivirus.

You are working on a national collaboration helping the NHS backed by HDRUK. This gives you substantial leverage with your institution. If you approach your local IT infrastructure team (via service ticket / email) and explain why you need it in a way that makes sense to both of you they will unblock it for you. If you need to escalate it via a manager do so. The issues comes from blanket policies being applied without thinking about the downstream negative consequences. If you build a positive relationship with that team they will trust you and the roadblock will dissapear.

You can also alternatively potentially get around the issue if you can install Docker on your local machine or access secure virtual machines elsewhere. If people need a guide on how to use that route then we can add it later on but we are keen to try and keep things as simple as possible and not add other tools in at this stage.

## Starting Minicondas

Instructions:

1. Open a command line / powershell or linux shell even windows terminal will work.
2. Type the word 'activate' and the shell should change to display (base) at the root.

Alternatively if you type 'prompt' in the search bar you should be able to launch a minicondas terminal directly that way.

## Downloading Repository

You should navigate to [Main Repo](https://github.com/MattStammers/hdruk_avoidable_admissions_collaboration_docs)

- If you are new to this I recommend pressing the code button and downloading the zip file to your own machine and unzipping it there.

- If you want to do this in a more scalable manner I recommend cloning the repo to your local machine with the command:

`git clone https://github.com/MattStammers/hdruk_avoidable_admissions_collaboration_docs`

This single command will work well but you will need to download git if you don't have it yet. Go here to get it: [Download Git](https://git-scm.com/downloads)

Then you are ready to move on to stage 2.
