# News Bias and reliability in Wikipedia

This repository offers the code we used in the project *News Bias and reliability in Wikipedia*.

Please find the code in the file *Code*, in this file, we list 5 files as below:
1. [Supplement news google sources](Code/get_news_google_source.py): Supplement the data from news google.

    1. This script is used for the sources from news.google.com, we use the link to search and find out what news outlet it belongs to.
    2. The result will be used in the second block of Analysis.py.
2. [Extracting data from Media Bias Monitor](Code/get_bais_form_MM.py ): Extract data from Media Bias Monitor(MBM).

    1. Read the paper for [Media Bias Monitor](https://www.aaai.org/ocs/index.php/ICWSM/ICWSM18/paper/viewFile/17878/17020)) and you can find more details about it.

    2. This process is divided into two steps. Firstly, we use the domain name in our dataset to search in the Media Bias Monitor, then we could get the interest_id for the news outlet which we could use to extract its bias information. Secondly, use the API and interest_id we got in the first step to extract the bias data from Media Bias Monitor.
    3. The result will be *"MM_page1.pkl"* and *MM_page2.pkl* and they can be used to match domain and bias score. 

3. [Extracting data from Media Bias Fact Check](Code/get_reliability_form_MBFC.py ): Extract data from Media Bias Fact Check(MBFC).

    1. We extract the reliability of news outlets from [Media Bias Fact Check](https://mediabiasfactcheck.com/). Executing script and we will get the news outlets' domain name and their reliability

    2. The result will be *"mbfc.xlsx"*, which can be used in Analysis.py to equip domains in our dataset with reliability.

4. [Example of MBM page2](Code/example_MBM_page2.txt): Example of MBM page2.

    1. Here we provide an example of the Media Bias Monitor page2 to make it easy to understand.

5. [Analysis](Code/Analysis.py): Complete analysis of our research.

    1. This script contains 3 blocks: read the whole dataset on Wikipedia, analysis the dataset and Regression analysis.
    
    2. Block 1: Read the whole dataset of Wikipedia
        1. You need to read the *Wikipedia Citations* dataset and download the [Wikipedia Citations dataset **minimal**](https://github.com/Harshdeep1996/cite-classifications-wiki) and store it in the folder and name it as "minimal_dataset.parquet".
        2. Execute the first part script to read the main dataset we need.
    
    3. Block 2: Analysis of the dataset.
        1. In this block we firstly clean up our dataset. Including cleaning the sources with "archive.com" and "news.google.com" and extracting the domain name from the URL.
        2. Secondly, we equip our domain name with bias from Media Bias Monitor and we plot the related plots.
        3. We equip our data with Wikipedia topics and WikiProjects to analyse the relationship between them and bias. Related plots included.
        4. We equip the data with reliability from Media Bias Fact Check and do related analysis on them and plots.
    
    4. Block 3: Regression analysis.
         1. After combining all the variables, we use the regression analysis to explore the relationship between bias and reliability. Here we only use the macro topics and top10 WikiProjects. 
