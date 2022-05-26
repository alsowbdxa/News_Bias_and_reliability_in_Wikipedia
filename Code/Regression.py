import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.formula.api import ols #加载ols模型

#firstly we use domain name to match bias score and topics, project and reliability, and get citations_bias_reg, which size is 3041283
citations_bias_reg = pd.merge(citations_bias_factual,match,left_on='domain_x',right_on='domain',how='left')# size is 3041283
#then we focus on bias score and topic, wiki project and reliability
citations_bias_reg = citations_bias_reg[['bias_score_avg','new_topic','wk_project','factual']]
#and we also creat a dataset which drop all the nan.
citations_bias_reg_notnull = citations_bias_reg.dropna()#604459

#then we are going deal with topics and wiki projects

#approach 1： use fractional counting for topic and only keep the main topics
def reg_topic(x):
    c = {'Geography':0,'Culture':0,'History_and_Society':0,'STEM':0}  
    t = eval(x)
    t0 = [i.split('.')[0] for i in t[0]]
    frac_t = [i/sum(t[1]) for i in t[1]]
    for i in range(len(t0)):
        c[t0[i]]+=frac_t[i]
    l.append(list(c.values()))
    
#approach 2：if one topic exist, we give it 1,if not, we give 0, this don't use fractional counting
def reg_topic(x):
    c = {'Geography':0,'Culture':0,'History_and_Society':0,'STEM':0}  
    t = eval(x)
    t0 = list(set([i.split('.')[0] for i in t[0]]))
    for i in t0:
        c[i]+=1
    l.append(list(c.values()))
    
l=[]
citations_bias_reg_notnull['new_topic'].progress_apply(lambda x:reg_topic(x))
r_topic = pd.DataFrame(l)
r_topic.columns = ['Geography','Culture','History_and_Society','STEM']
citations_bias_reg_notnull['Geopgraphy']=r_topic['Geography']
citations_bias_reg_notnull['Culture']=r_topic['Culture']
citations_bias_reg_notnull['History_and_Society']=r_topic['History_and_Society']
citations_bias_reg_notnull['STEM']=r_topic['STEM']
# after that we get 4 columns which seperately contains 4 main topics, it could be used for later regression.

#for wiki project
#approach 1: use fractional counting for project and only keep top10 projects
def reg_project(x):
    c = dict(zip(top10_project,[0]*10))
    c['Other']=0
    t = eval(x)
    t1 = Counter([i if i in top10_project else 'Other' for i in t])
    for i in t1:
        c[i]+=t1[i]/len(t)
    l.append(list(c.values()))

#approach 2:only give 0 or 1 if the project exists
def reg_project(x):
    c = dict(zip(top10_project,[0]*10))
    c['Other']=0
    t = eval(x)
    t1 = list(set([i if i in top10_project else 'Other' for i in t]))
    for i in t1:
        c[i]+=1
    l.append(list(c.values()))

l=[]
citations_bias_reg_notnull['wk_project'].progress_apply(lambda x:reg_project(x))
r_project = pd.DataFrame(l)
r_project.columns = top10_project+['Other']
for i in top10_project+['Other']:
    citations_bias_reg_notnull[i]=r_project[i].to_list()
# after that we get 11 columns which seperately contains top10 projects and "Other", it could be used for later regression.

#rename the columns
citations_bias_reg_notnull.columns = ['bias_score_avg', 'new_topic', 'wk_project', 'factual', 'Geography',
       'Culture', 'History_and_Society', 'STEM', 'Biography', 'Medicine',
       'Biography_science_and_academia_work_group', 'United_States',
       'Articles_for_creation', 'Politics', 'India', 'Pharmacology', 'Lists',
       'Military_history', 'Other']

#start to regression
# First model: bias score and topics, STEM should be removed or not depends on the approach we use
#model_ols = smf.ols(formula="bias_score_avg ~ Geography + Culture + History_and_Society",data=citations_bias_reg_notnull)#with approach 1
model_ols = smf.ols(formula="bias_score_avg ~ Geography + Culture + History_and_Society + STEM",data=citations_bias_reg_notnull)#with approach 2
res_ols = model_ols.fit()
print(res_ols.summary())

# Second model: bias score ,topics and reliability
#model_ols = smf.ols(formula="bias_score_avg ~ C(factual, Treatment(reference='MOSTLY FACTUAL')) + Geography + Culture + History_and_Society",data=citations_bias_reg_notnull)#approach 1
model_ols = smf.ols(formula="bias_score_avg ~ C(factual, Treatment(reference='MOSTLY FACTUAL')) + Geography + Culture + History_and_Society + STEM",data=citations_bias_reg_notnull)#approach 2
res_ols = model_ols.fit()
print(res_ols.summary())

# Third model: bias score ,topics, reliability and projects
#model_ols = smf.ols(formula="bias_score_avg ~ C(factual, Treatment(reference='MOSTLY FACTUAL')) + Geography + Culture + History_and_Society + Biography + Medicine + Biography_science_and_academia_work_group + United_States + Articles_for_creation+ Politics + India + Pharmacology + Lists + Military_history",data=citations_bias_reg_notnull)#approach 1
model_ols = smf.ols(formula="bias_score_avg ~ C(factual, Treatment(reference='MOSTLY FACTUAL')) + Geography + Culture + History_and_Society + STEM + Biography + Medicine + Biography_science_and_academia_work_group + United_States + Articles_for_creation+ Politics + India + Pharmacology + Lists + Military_history + Other",data=citations_bias_reg_notnull)#approach 2
res_ols = model_ols.fit()
print(res_ols.summary())

