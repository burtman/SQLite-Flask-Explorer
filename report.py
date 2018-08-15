# coding: utf-8
from IPython.core.display import display,HTML
from imagestats import *
import tabulate
import math
import string
from numpy import sqrt
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
import functools
import warnings
warnings.filterwarnings('ignore')


def list_to_txt(name):
    if type(name)==list:
        string=[]
        for item in name:
            if item=='.*':
                item='[All]'
            item=item.replace('.*', '[Anything]').replace('_', ' ')
            string.append(item.title()) #.title() capitalizes the first letter of each word
        string=",\n".join(string)

    else:
        print "not list"
        string=name
        if string=='.*':
            string='[All]'
        string=string.replace('.*', '[Anything]')

    return string

def description_report(log,columns_tbl,filters=[],sigtest=False,confidence=0.9,fraction_digits=1,ecommerce_metrics=False,contains_product=True):
    col_name=["coded"]
    experiment_respondents=["Experiment Base (Base without Product filter)"]
    experiment_shareofchoice=["Share of choice"]
    experiment_penetration=["Penetration"]
    resp_opened=["Nb respondents opened"]
    experiment_openingrate=["Opening Rate"]
    experiment_totalchoices=["Total product bought in experiment"]
    experiment_totalbuyers=["Total number of buyers in experiment"]
    #experiment_conversionrate=["Conversion Rate (% bought on opened)"]

    base=["Base"]
    interactions=["Interactions"]
    visitors=["Unique Visitors & Buyers"]
    perc_visitors=["% visitors"]
    conversions=["Conversions"]
    conversion_rate=["% visitors bought"]
    time_spent=["Time Spent"]
    time_spent_descr=["Time Spent Description"]



    mask=[] #Reinitialise mask_main
    for filter_index in range(len(filters)):

        if filter_index==0:
            if (contains_product==False) & (filters[filter_index]['column']=='Product'):
                mask=log[filters[filter_index]['column']]==filters[filter_index]['content']
            else:
                mask=log[filters[filter_index]['column']].str.contains(filters[filter_index]['content'])
        else:
            if (contains_product==False) & (filters[filter_index]['column']=='Product'):
                mask = [x and y for x,y in zip(mask,log[filters[filter_index]['column']]==filters[filter_index]['content'])]
            else:
                # Looking for 'content' in 'column' and adding (and) to the previous mask
                mask = [x and y for x,y in zip(mask,log[filters[filter_index]['column']].str.contains(filters[filter_index]['content']))]

    for filter_index in range(len(filters)):

        if filter_index==0:
            mask_exp=log[filters[filter_index]['column']].str.contains(filters[filter_index]['content'])
        else:
            # Looking for 'content' in 'column' and adding (and) to the previous mask
            if filters[filter_index]['column']!='Product':
                mask_exp = [x and y for x,y in zip(mask_exp,log[filters[filter_index]['column']].str.contains(filters[filter_index]['content']))]


    for tbl_col in columns_tbl:

        experiment_base_size=len(log[mask_exp][
           log['Action'].isin(['pageview','bought'])
        ]['RespondentId'].unique())

        col_name.append(list_to_txt(tbl_col['name']))
        #import pdb;pdb.set_trace()

        base_size=len(log[mask][
           log['Action'].isin(['pageview','bought'])
        ]['RespondentId'].unique())

        base.append(base_size)
        experiment_respondents.append(experiment_base_size)



        if (tbl_col['type']=="group") & (tbl_col['name']=="video"):
            interactions.append(len(log[mask][
                          log['Action'].isin(['videogallery','videoview'])]))

            nb_visitors=len(log[mask][log['Action'].isin(['videogallery','videoview'])]
                                ['RespondentId'].unique())

            visitors.append(nb_visitors)

            unique_visitors_id=log[mask][(log['Action'].isin(['videogallery','videoview']))]['RespondentId'].unique()
            bought=len(log[mask][(log['RespondentId'].isin(list(unique_visitors_id)))
                       & (log['Action']=='bought')
                    & (log['Bought']==1)]['RespondentId'].unique())

            conversions.append(bought)

            if nb_visitors!=0:
                conversion_rate.append('{:.{}%}'.format(float(bought)/float(nb_visitors),fraction_digits))
                perc_visitors.append('{:.{}%}'.format(float(nb_visitors)/float(base_size),fraction_digits))
                time_spent.append('{:.{}f}'.format(
                    float(log[mask][
                    log['Action'].isin(['videogallery','videoview'])]['timespent'].sum())/
                                  float(len(log[mask][log['Action'].isin(['videogallery','videoview'])])),fraction_digits))
            else:
                conversion_rate.append('{:.{}%}'.format(0,fraction_digits))
                perc_visitors.append('{:.{}%}'.format(0,fraction_digits))
                time_spent.append('{:.{}f}'.format(float(0),fraction_digits))

        elif (tbl_col['type']=="group") & (tbl_col['name']=="secondary"):


            interactions.append(len(log[mask][
                          (log['Action'].isin(['imagegallery','imagezoomin']))
                          & (log['img_pos']>=2)]))
            nb_visitors=len(log[mask][
                          (log['Action'].isin(['imagegallery','imagezoomin']))
                          & (log['img_pos']>=2)]
                                ['RespondentId'].unique())
            visitors.append(nb_visitors)

            unique_visitors_id=log[mask][(log['Action'].isin(['imagegallery','imagezoomin'])) & (log['img_pos']>=2)]['RespondentId'].unique()
            bought=len(log[mask][(log['RespondentId'].isin(list(unique_visitors_id)))
                    #& (log['Action'].isin(['imagegallery','imagezoomin']))
                    & (log['img_pos']>=2)
                    & (log['Bought']==1)]['RespondentId'].unique())

            conversions.append(bought)

            if nb_visitors!=0:
                conversion_rate.append('{:.{}%}'.format(float(bought)/float(nb_visitors),fraction_digits))
                perc_visitors.append('{:.{}%}'.format(float(nb_visitors)/float(base_size),fraction_digits))
                time_spent.append('{:.{}f}'.format(
                    float(log[mask][
                    (log['Action'].isin(['imagegallery','imagezoomin'])) & (log['img_pos']>=2)]['timespent'].sum())/
                                  float(len(log[mask][log['img_pos']>=2])),fraction_digits))
            else:
                conversion_rate.append('{:.{}%}'.format(0,fraction_digits))
                perc_visitors.append('{:.{}%}'.format(0,fraction_digits))
                time_spent.append('{:.{}f}'.format(float(0),fraction_digits))

        elif (tbl_col['type']=="group") & (tbl_col['name']=="All pictures"):

            unique_visitors_id=log[mask][log['Action'].isin(['imagegallery','imagezoomin'])]['RespondentId'].unique()
            interactions.append(len(log[mask][log['Action'].isin(['imagegallery','imagezoomin'])]))

            nb_visitors=len(log[mask][log['Action'].isin(['imagegallery','imagezoomin'])]
                                ['RespondentId'].unique())
            visitors.append(nb_visitors)

            bought=len(log[mask][(log['RespondentId'].isin(list(unique_visitors_id)))
                       #& (log['Action'].isin(['imagegallery','imagezoomin']))
                    & (log['Bought']==1)]['RespondentId'].unique())

            conversions.append(bought)

            if nb_visitors!=0:
                conversion_rate.append('{:.{}%}'.format(float(bought)/float(nb_visitors),fraction_digits))
                perc_visitors.append('{:.{}%}'.format(float(nb_visitors)/float(base_size),fraction_digits))
                time_spent.append('{:.{}f}'.format(
                    float(log[mask][log['Action'].isin(['imagegallery','imagezoomin'])]['timespent'].sum())/
                                  float(len(log[mask][log['Action'].isin(['imagegallery','imagezoomin'])])),fraction_digits))
            else:
                conversion_rate.append('{:.{}%}'.format(0,fraction_digits))
                perc_visitors.append('{:.{}%}'.format(0,fraction_digits))
                time_spent.append('{:.{}f}'.format(0,fraction_digits))

        elif tbl_col['type']=="img_pos":
            pos=tbl_col['name']
            unique_visitors_id=log[mask][(log['Action'].isin(['imagegallery','imagezoomin'])) & (log['img_pos']==pos)]['RespondentId'].unique()
            interactions.append(len(log[mask][(
                          log['Action'].isin(['imagegallery','imagezoomin']))
                          & (log['img_pos']==pos)]))
            nb_visitors=len(log[mask][
                        (log['Action'].isin(['imagegallery','imagezoomin']))
                          & (log['img_pos']==pos)
                         ]['RespondentId'].unique())

            visitors.append(nb_visitors)

            bought=len(log[mask][(log['RespondentId'].isin(list(unique_visitors_id)))
                       #& (log['Action'].isin(['imagegallery','imagezoomin']))
                    & (log['Bought']==1)]['RespondentId'].unique())

            conversions.append(bought)

            if nb_visitors!=0:
                conversion_rate.append('{:.{}%}'.format(float(bought)/float(nb_visitors),fraction_digits))
                perc_visitors.append('{:.{}%}'.format(float(nb_visitors)/float(base_size),fraction_digits))
                time_spent.append('{:.{}f}'.format(float(log[mask][
                    (log['Action'].isin(['imagegallery','imagezoomin'])) & (log['img_pos']==pos)]['timespent'].sum())/
                                  float(len(log[mask][log['img_pos']==pos])),fraction_digits))
            else:
                conversion_rate.append('{:.{}%}'.format(0,fraction_digits))
                perc_visitors.append('{:.{}%}'.format(0,fraction_digits))
                time_spent.append('{:.{}f}'.format(float(0),fraction_digits))

        elif tbl_col['type']=='action':
            action=tbl_col['name']
            interactions.append(len(log[mask][log['Action'].isin(action)]))

            unique_visitors_id=log[mask][log['Action'].isin(action)]['RespondentId'].unique()
            nb_visitors=len(unique_visitors_id)
            visitors.append(nb_visitors)

            bought=len(log[mask][(log['RespondentId'].isin(list(unique_visitors_id)))
                        #& (log['Action'].isin(action))
                    & (log['Bought']==1)]['RespondentId'].unique())


            conversions.append(bought)

            choices=len(log[mask][(log['RespondentId'].isin(list(unique_visitors_id)))
                       & (log['Action']=='bought')
                    & (log['Bought']==1)])

            experiment_choices=len(log[mask_exp][(log['Action'].isin(action))
                    & (log['Bought']==1)])
            experiment_bought=len(log[mask_exp][(log['Action'].isin(action))
                    & (log['Bought']==1)]['RespondentId'].unique())

            opened=len(log[mask][(log['RespondentId'].isin(list(unique_visitors_id)))
               & (log['Action'].isin(['pageview']))
            ]['RespondentId'].unique())

            resp_opened.append(opened)
            experiment_totalchoices.append(experiment_choices)
            experiment_totalbuyers.append(experiment_bought)

            if nb_visitors!=0:
                conversion_rate.append('{:.{}%}'.format(float(bought)/float(nb_visitors),fraction_digits))
                perc_visitors.append('{:.{}%}'.format(float(nb_visitors)/float(base_size),fraction_digits))
                time_spent.append(float('{:.{}}'.format(float(log[mask][log['Action'].isin(action)]['timespent'].sum())/
                                  float(len(log[mask][log['Action'].isin(action)])),fraction_digits+1)))
            else:
                conversion_rate.append('{:.{}%}'.format(0,fraction_digits))
                perc_visitors.append('{:.{}%}'.format(0,fraction_digits))
                time_spent.append(float('{:.{}}'.format(float(0),fraction_digits+1)))

            if experiment_base_size!=0:
                experiment_openingrate.append('{:.{}%}'.format(float(opened)/float(experiment_base_size),fraction_digits))
            else:
                experiment_openingrate.append('{:.{}%}'.format(0,fraction_digits))

            if experiment_choices!=0:
                experiment_shareofchoice.append('{:.{}%}'.format(float(choices)/float(experiment_choices),fraction_digits))
            else:
                experiment_shareofchoice.append('{:.{}%}'.format(0,fraction_digits))

            if experiment_bought!=0:
                experiment_penetration.append('{:.{}%}'.format(float(bought)/float(experiment_bought),fraction_digits))
            else:
                experiment_penetration.append('{:.{}%}'.format(0,fraction_digits))

    if ecommerce_metrics:
        data = [#
                col_name,

                experiment_respondents,
                experiment_openingrate,
                resp_opened,

                visitors,
                conversion_rate,
                conversions,

                experiment_totalchoices,
                experiment_shareofchoice,

                experiment_totalbuyers,
                experiment_penetration,

                time_spent]
    else:
           data = [#
                    col_name,
                    base,
                    interactions,
                    visitors,
                    perc_visitors,
                    conversions,
                    conversion_rate,
                    time_spent]

    # Turn list of lists in a dataframe
    dfr=pd.DataFrame(data)
    # Set the first row as the dataframe header (str is added to avoid "unhashable type" error with titles that include [''])
    col_names=[str(col) for col in dfr.iloc[0]]
    dfr.columns=col_names
    #Reset the rows index and drop the first line
    dfr=dfr.reindex(dfr.index.drop(0))
    #Add index column to fit the ecommerce metrics sigtest format
    dfr['index']=0
    #Re shuffle the column order
    dfr=dfr[['index']+col_names]

    #import pdb;pdb.set_trace()
    if sigtest:
        return sigtest_ecommerce_metrics(dfr,confidence)
    else:
        return dfr

def zTest(p1,n1,p2,n2):
	# Parametric method: Z-test
	numerator = (p1/n1) - (p2/n2)
	p_common = (p1+p2) / (n1+n2)
	denominator = sqrt(p_common * (1-p_common) * (1/n1 + 1/n2))
	z_score = numerator / denominator
	p_value = stats.norm.sf(z_score)
	return p_value

def perc2float(x):
    if isinstance(x, float):
        return x
    else:
        return float(x.strip('%'))/100

def str2float(x):
    return float(x)

def sigtest_ecommerce_metrics(df,confidence=0.90):
    df_original=df.copy()
    df=df.set_index('coded').drop('index',axis=1)
    #import pdb;pdb.set_trace()

    #Base sizes from str to float
    df.iloc[0,:]=df.iloc[0,:].apply(lambda x: str2float(x))

    #Other percentages from str to float
    for i in range(len(df.index)-1):
        df.iloc[i+1,:]=df.iloc[i+1,:].apply(lambda x: perc2float(x) if isinstance(x, str) else x)
    # We create an empty dataframe with the same shape
    sigvalues = np.empty(shape=(df.shape[0],len(df.columns)),dtype=object)

    # We compute the sum of the base sizes
    n_total=df.iloc[0,:].sum()
    # We iterate through every row (i.e brands)

    for row_num in range(len(df.index)-1):

        row_percs=df.iloc[row_num+1,:]
        base_sizes=df.iloc[0,:]
        # We iterate trhough columns
        for p1,n1,col_num in zip(row_percs,base_sizes,range(len(row_percs))):
            # We iterate trhough columns again to test each against each other from the same row
            for p2,n2,col_num2 in zip(row_percs,base_sizes,range(len(row_percs))):

                pvalue=zTest(p1*n1,n1,p2*n2,n2)


                if str(sigvalues[row_num+1,col_num])=='None':
                    updated_string= str('{:.0%}'.format(float(df.iloc[row_num+1,col_num])))
                    sigvalues[row_num+1,col_num] = updated_string

                if pvalue < 1-confidence:
                    cell_value = str(sigvalues[row_num+1,col_num])
                    updated_string = cell_value+string.ascii_letters[col_num2]
                    sigvalues[row_num+1,col_num] = updated_string
    sigvalues=pd.DataFrame(sigvalues,columns=[name+' ('+string.ascii_letters[num]+')' for num,name in enumerate(df.columns.tolist())],index=df.index)

    sigvalues.iloc[0,:]=df.iloc[0,:].tolist()

    #If the row does not contain any percentage (str) we keep the original values and do not keep the computed sig tests
    for i in range(len(df_original.index)):
        if not any(isinstance(x, str) for x in df_original.iloc[i,:].tolist()[2:]):
            sigvalues.iloc[i,:]=df_original.iloc[i,:].tolist()[2:]

    sigvalues['Sigtest']=df.index.tolist()


    sigvalues=sigvalues.set_index('Sigtest')
    return sigvalues
