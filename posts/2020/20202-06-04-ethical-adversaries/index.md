## Why should we care about fair models?
Machine learning eases the deployment of systems that tackles various tasks: spam filtering, image recognition, gesture recognition, etc.
One of the most trendy applications is decision support. After collecting data on people and their context, these systems give recommendations on who should get a loan, predict who may commit subsequent offences, etc. However, this support can have detrimental consequences.
Well-studied examples include the COMPAS system that predicts the recidivism of pre-trial inmates~\citep{angwinMachineBiasThere2016, chouldechovaFairPredictionDisparate2017} or accepting credit applications, or more recently the issues with Apple's credit card that resulted in vastly lower spending limits for women. Such systems may amplify the prevalent situation by imposing more expensive loans to African-American people, who then fail to repay them more often~\citep{overdorfQuestioningAssumptionsFairness2018, ensign2017}. These ``positive" feedback loops should be detected and mitigated.  

Training a machine learning model can be costly, is sensitive to the data quality, and may result in a complex model. Hence, the decision process may fail to be transparent, which ushers in discrimination or unfair treatment for protected groups. But how to perform this assessment when decisions are often neither interpretable nor intuitive?

## Architecture

<div class="col-12"> <img class="figure-img img-fluid" src="architecture.png"/> </div>

### The reader

### the feeder

## Results

<div class="row">
    <div class="col-md-4 col-xs-12"> <img class="figure-img img-fluid" src="utility.svg"/> </div>
    <div class="col-md-4 col-xs-12"> <img class="figure-img img-fluid" src="fairness_eo.svg"/> </div>
    <div class="col-md-4 col-xs-12"> <img class="figure-img img-fluid" src="fairness_dpr.svg"/> </div>
</div>


## Selected citations