# importing numpy for maths operations
import numpy as np

# importing pandas for file handling
import pandas as pd

# read data
df1 = pd.read_csv('input1.csv')
df2 = pd.read_csv('input2.csv')

# creating a leaderbord class. it takes two parameters (dataframe1 , dataframe2)


class Leaderbord:

    # constructing the class
    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2
        self.total_df = None
        self.repair_dataset()  # function performs activity like rename, replace etc in df2

        # running functions to create output dataframes
        self.output1 = self.get_teamwise()
        self.output2 = self.get_individual()

    #   function  calculate rank from 1 to ..
    def calculate_rank(self, df, column_name='Rank'):
        ''' function take two arguments 
            calculate_rank(pandas dataframe , column name of rank column, default is "Rank")
            returns pandas dataframe
        '''
        # calculate no of rows in dataframe
        total_rank = list(range(1, df.shape[0]+1))
        # creatin rank column at index 0
        df.insert(0, column_name, total_rank)
        # reseting index of dataframe from 0 and droping duplicate index column
        df = df.reset_index(drop=True)
        return df

    def repair_dataset(self) -> None:
        ''' rename , replace df2 '''
        df2 = self.df2.rename(
            columns={'Team Name': 'team_name', 'User ID': 'uid'})  # renaming dataframe
        df2.replace('Brandtech Lab', 'BrandTech Lab',
                    inplace=True)  # replacing one flaw in data
        # merging two dataframe
        self.total_df = pd.merge(df1, df2, on="uid", how='inner')
        self.df2 = df2


    # converting pandas dataframe into excel format
    def get_in_excel(self):
        #     writing file
        with pd.ExcelWriter("output.xlsx") as excelfile:
            self.output2.to_excel(
                excelfile, sheet_name="Leaderboard Individual (Output)", index=False)
            self.output1.to_excel(
                excelfile, sheet_name="Leaderboard TeamWise (Output)", index=False)
    
    def get_teamwise(self):
        ''' 
        output as self.output1
        '''
        # finding average of no. of statements and results from merged dataframe
        output = self.total_df.groupby(
            'team_name', as_index=False).mean().round(2)
        output.drop(columns=['uid'], inplace=True)
        # sorting data
        output.sort_values(by=['total_statements', 'total_reasons', 'team_name'], ascending=[
                           False, False, True], inplace=True)

        output = self.calculate_rank(output, 'Team Rank')
        # renaming columns
        output = output.rename(columns={'team_name': 'Thinking Teams Leaderboard',
                                        'total_statements': 'Average Statements', 'total_reasons': 'Average Reasons'})
        return output

    def get_individual(self):
        '''
        output as self.output2
        '''
        output = self.df1.copy()  # creating copy of dataframe
        old_df = self.df1
        # total number of statements and reasons
        output['total'] = output['total_statements']+output['total_reasons']
        # tuning name for sorting purpose
        output['name'] = output.name.apply(lambda x: x.upper())
        output = output.sort_values(by=['total', 'name'], ascending=[
                                    False, True])  # sorting data
        output = self.calculate_rank(output, 'Rank')
        # merging dataframe to get original names
        output = pd.merge(output, old_df, on='uid', how='inner')
        # selecting columns
        output = output[['Rank', 'name_y', 'uid',
                         'total_statements_x', 'total_reasons_y']]
        return output.rename(
            columns={
                'name_y': 'Name',
                'uid': 'UID',
                'total_statements_x': 'No. of Statements',
                'total_reasons_y': 'No. of Reasons',
            }
        )




leaderbord = Leaderbord(df1, df2)
leaderbord.get_in_excel()
print(leaderbord.get_individual())
print(leaderbord.get_teamwise())
