import pandas as pd
import numpy as np

cats = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
        'December']
cats1 = ['January', 'January', 'February', 'February', 'March', 'March', 'April', 'April', 'May', 'May', 'June', 'June',
         'July', 'July', 'August', 'August',
         'September', 'September', 'October', 'October', 'November', 'November', 'December', 'December']
labels = ['18-29', '30-39', '40-49', '50-59', '60-69', '70+']
bins = [18, 30, 40, 50, 60, 70, 120]


class MainClass:

    def oreder_series_months(self, seriess):
        seriess.index = pd.CategoricalIndex(seriess.index, categories=cats,
                                            ordered=True)
        return seriess.sort_index()

    def convert_dates(self, dataFrame, convertby):
        dataFrame['Transaction Date'] = dataFrame['Transaction Date'].dt.strftime('%B')
        return dataFrame

    def conver_age_to_agegroups(self, dataFrame):
        dataFrame['agerange'] = pd.cut(dataFrame["Customer Age"], bins, labels=labels, include_lowest=True)
        return dataFrame

    def merge_profit_series_in_dataframe(self, profitA, profitB, label1, label2):
        trmpdfA = pd.DataFrame({label1: profitA.index, label2: profitA.values,
                                'group': 'A'})  # Convert Series to dataframe
        trmpdfB = pd.DataFrame({label1: profitB.index, label2: profitB.values,
                                'group': 'B'})  # Convert Series to dataframe
        return pd.concat([trmpdfA, trmpdfB])

    def merge_conversion_series_in_dataframe(self, conversionA, conversionB, label):
        trmpdfA = pd.DataFrame({label: conversionA.index, 'conversion': conversionA.values,
                                'group': 'A'})  # Convert Series to dataframe
        trmpdfB = pd.DataFrame({label: conversionB.index, 'conversion': conversionB.values,
                                'group': 'B'})  # Convert Series to dataframe
        return pd.concat([trmpdfA, trmpdfB])

    def merge_total_price_series_in_df(self, totalPriceA, totalPriceB, label):
        trmpdfA = pd.DataFrame({label: totalPriceA.index, 'revenue': totalPriceA.values,
                                'group': 'A'})  # Convert Series to dataframe
        trmpdfB = pd.DataFrame({label: totalPriceB.index, 'revenue': totalPriceB.values,
                                'group': 'B'})  # Convert Series to dataframe
        return pd.concat([trmpdfA, trmpdfB])

    def order_dataframe_months(self, myframe):
        myframe["months"] = pd.CategoricalIndex(myframe["months"], categories=cats,
                                                ordered=True)
        return myframe

    def merge_percentagelist_in_df(self, listA, listB, months, lable):
        tempDfA = pd.DataFrame({lable: months, 'percentage': listA, 'group': 'A'})
        tempDfB = pd.DataFrame({lable: months, 'percentage': listB, 'group': 'B'})
        return pd.concat([tempDfA, tempDfB])

    def get_revenue_percentage(self, revenueA, revenueB, total_revenue):
        rA = []
        rB = []
        for itemA, itemB in zip(revenueA.iteritems(), revenueB.iteritems()):
            rA.append(round((itemA[1] * 100) / total_revenue, 2))
            rB.append(round((itemB[1] * 100) / total_revenue, 2))
        temprA = pd.DataFrame({'months': revenueA.index, 'percentage': rA, 'group': 'A'})
        temprB = pd.DataFrame({'months': revenueA.index, 'percentage': rB, 'group': 'B'})
        return pd.concat([temprA, temprB])

    def get_revenue_percent_groups(self, revenueA, total_r, group):
        rA = []
        for itemA in revenueA.iteritems():
            rA.append(round((itemA[1] * 100) / total_r, 2))
        return pd.DataFrame({'months': revenueA.index, 'percentage': rA, 'group': group})

    def get_dataframe_for_netProfit_chart(self, df_A, df_B):
        group_by_month_profitA = df_A.groupby(df_A['months'])['Profit'].mean().round(2)
        group_by_month_profitA = self.oreder_series_months(group_by_month_profitA)
        group_by_month_profitB = df_B.groupby(df_B['months'])['Profit'].mean().round(2)
        group_by_month_profitB = self.oreder_series_months(group_by_month_profitB)

        group_by_weekly_profitA = df_A.groupby(df_A['weeks'])['Profit'].mean().round(2)
        group_by_weely_profitB = df_B.groupby(df_B['weeks'])['Profit'].mean().round(2)

        profitA_B_monthly = self.merge_profit_series_in_dataframe(group_by_month_profitA,
                                                                  group_by_month_profitB,
                                                                  'months', 'profits')
        profitA_B_weekly = self.merge_profit_series_in_dataframe(group_by_weekly_profitA,
                                                                 group_by_weely_profitB,
                                                                 'weeks', 'profits')

        grop_by_ageA = df_A.groupby(df_A['Age Groups'])['Profit'].mean().round(2)
        grop_by_ageB = df_B.groupby(df_B['Age Groups'])['Profit'].mean().round(2)
        profit_A_B_agewise = self.merge_profit_series_in_dataframe(grop_by_ageA, grop_by_ageB, "age groups", 'profits')

        grop_by_creditA = df_A.groupby(df_A['Credit Groups'])['Profit'].mean().round(2)
        grop_by_creditB = df_B.groupby(df_B['Credit Groups'])['Profit'].mean().round(2)
        profitA_B_Crediwise = self.merge_profit_series_in_dataframe(grop_by_creditA, grop_by_creditB, "credit groups",
                                                                    'profits')

        group_by_vehicle_valueA = df_A.groupby(df_A['Vehiclevalue Groups'])['Profit'].mean().round(2)
        group_by_vehicle_valueB = df_B.groupby(df_B['Vehiclevalue Groups'])['Profit'].mean().round(2)
        profit_A_B_vv = self.merge_profit_series_in_dataframe(group_by_vehicle_valueA, group_by_vehicle_valueB,
                                                              "vehicle value", 'profits')

        group_by_vehicle_valueA = df_A.groupby(df_A['Mileage Groups'])['Profit'].mean().round(2)
        group_by_vehicle_valueB = df_B.groupby(df_B['Mileage Groups'])['Profit'].mean().round(2)
        profit_A_B_vehicle_mile = self.merge_profit_series_in_dataframe(group_by_vehicle_valueA,
                                                                        group_by_vehicle_valueB, "mileage", 'profits')

        group_by_licence_A = df_A.groupby(df_A['Licence Groups'])['Profit'].mean().round(2)
        group_by_licence_B = df_B.groupby(df_B['Licence Groups'])['Profit'].mean().round(2)
        profit_A_B_licence = self.merge_profit_series_in_dataframe(group_by_licence_A, group_by_licence_B,
                                                                   "licence length", 'profits')

        return profitA_B_monthly, profitA_B_weekly, profit_A_B_agewise, \
               profitA_B_Crediwise, profit_A_B_vv, profit_A_B_vehicle_mile, profit_A_B_licence

    def get_dataframes_for_conversion_chart(self, df_A, df_B, counts_A, counts_B):
        group_by_month_conversionA = df_A.groupby(df_A['months'])['Sale Indicator'].mean().round(2)
        group_by_month_conversionA = self.oreder_series_months(group_by_month_conversionA)
        group_by_month_conversionB = df_B.groupby(df_B['months'])['Sale Indicator'].mean().round(2)
        group_by_month_conversionB = self.oreder_series_months(group_by_month_conversionB)

        group_by_week_conversionA = df_A.groupby(df_A['weeks'])['Sale Indicator'].mean().round(2)
        group_by_week_conversionB = df_B.groupby(df_B['weeks'])['Sale Indicator'].mean().round(2)
        cpnversionA_B_monthly = self.merge_profit_series_in_dataframe(group_by_month_conversionA,
                                                                      group_by_month_conversionB, "months",
                                                                      'conversion')
        conversionA_B_weekly = self.merge_profit_series_in_dataframe(group_by_week_conversionA,
                                                                     group_by_week_conversionB, "weeks", 'conversion')
        percentageA = []
        percentageB = []
        for totalA, convertedA, totalB, convertedB in zip(counts_A.iteritems(),
                                                          group_by_month_conversionA.iteritems(),
                                                          counts_B.iteritems(),
                                                          group_by_month_conversionB.iteritems()):
            percentageA.append(round((convertedA[1] * 100) / totalA[1], 2))
            percentageB.append(round((convertedB[1] * 100) / totalB[1], 2))
        percentage_A_B = self.merge_percentagelist_in_df(percentageA, percentageB, counts_A.index, "months")

        age_countsA = df_A['Age Groups'].value_counts()
        age_countsA.index = pd.CategoricalIndex(age_countsA.index, categories=labels,
                                                ordered=True)
        age_countsB = df_B['Age Groups'].value_counts()
        age_countsB.index = pd.CategoricalIndex(age_countsB.index, categories=labels,
                                                ordered=True)
        grop_by_ageA = df_A.groupby(df_A['Age Groups'])['Sale Indicator'].mean().round(2)
        grop_by_ageB = df_B.groupby(df_B['Age Groups'])['Sale Indicator'].mean().round(2)
        conversion_A_B_agewise = self.merge_profit_series_in_dataframe(grop_by_ageA, grop_by_ageB, "age groups",
                                                                       'conversion')

        grop_by_creditA = df_A.groupby(df_A['Credit Groups'])['Sale Indicator'].mean().round(2)
        grop_by_creditB = df_B.groupby(df_B['Credit Groups'])['Sale Indicator'].mean().round(2)
        conversionA_B_Crediwise = self.merge_profit_series_in_dataframe(grop_by_creditA, grop_by_creditB,
                                                                        "credit groups",
                                                                        'conversion')

        group_by_vehicle_valueA = df_A.groupby(df_A['Vehiclevalue Groups'])['Sale Indicator'].mean().round(2)
        group_by_vehicle_valueB = df_B.groupby(df_B['Vehiclevalue Groups'])['Sale Indicator'].mean().round(2)
        conversion_A_B_vv = self.merge_profit_series_in_dataframe(group_by_vehicle_valueA, group_by_vehicle_valueB,
                                                                  "vehicle value", 'conversion')

        group_by_vehicle_valueA = df_A.groupby(df_A['Mileage Groups'])['Sale Indicator'].mean().round(2)
        group_by_vehicle_valueB = df_B.groupby(df_B['Mileage Groups'])['Sale Indicator'].mean().round(2)
        conversion_A_B_vehicle_mile = self.merge_profit_series_in_dataframe(group_by_vehicle_valueA,
                                                                            group_by_vehicle_valueB, "mileage",
                                                                            'conversion')

        group_by_licence_A = df_A.groupby(df_A['Licence Groups'])['Sale Indicator'].mean().round(2)
        group_by_licence_B = df_B.groupby(df_B['Licence Groups'])['Sale Indicator'].mean().round(2)
        conversion_A_B_licence = self.merge_profit_series_in_dataframe(group_by_licence_A, group_by_licence_B,
                                                                       "licence length", 'conversion')

        # percentageA.clear()
        # percentageB.clear()
        # for totalA, convertedA, totalB, convertedB in zip(age_countsA.iteritems(),
        #                                                   grop_by_ageA.iteritems(),
        #                                                   age_countsB.iteritems(),
        #                                                   grop_by_ageB.iteritems()):
        #     percentageA.append(round((convertedA[1] * 100) / totalA[1], 2))
        #     percentageB.append(round((convertedB[1] * 100) / totalB[1], 2))
        #
        # age_percentage = self.merge_percentagelist_in_df(percentageA, percentageB, age_countsA.index, "age groups")

        return cpnversionA_B_monthly, conversionA_B_weekly, percentage_A_B, conversion_A_B_agewise, \
               conversionA_B_Crediwise, conversion_A_B_vv, conversion_A_B_vehicle_mile, conversion_A_B_licence

    def get_dataframes_for_revenue_charts(self, df_A, df_B):
        group_by_monthly_total_priceA = df_A.groupby(df_A['months'])['Total Price'].mean().round(2)
        group_by_monthly_total_priceA = self.oreder_series_months(group_by_monthly_total_priceA)
        group_by_monthly_total_priceB = df_B.groupby(df_B['months'])['Total Price'].mean().round(2)
        group_by_monthly_total_priceB = self.oreder_series_months(group_by_monthly_total_priceB)

        group_by_weekly_total_priceA = df_A.groupby(df_A['weeks'])['Total Price'].mean().round(2)
        group_by_weekly_total_priceB = df_B.groupby(df_B['weeks'])['Total Price'].mean().round(2)

        revenueA_B_monthly = self.merge_profit_series_in_dataframe(group_by_monthly_total_priceA,
                                                                   group_by_monthly_total_priceB, 'months', 'revenue')
        revenueA_B_weekly = self.merge_profit_series_in_dataframe(group_by_weekly_total_priceA,
                                                                  group_by_weekly_total_priceB, 'weeks', 'revenue')

        grop_by_ageA = df_A.groupby(df_A['Age Groups'])['Total Price'].mean().round(2)
        grop_by_ageB = df_B.groupby(df_B['Age Groups'])['Total Price'].mean().round(2)
        revenue_A_B_agewise = self.merge_profit_series_in_dataframe(grop_by_ageA, grop_by_ageB, "age groups", 'revenue')

        grop_by_creditA = df_A.groupby(df_A['Credit Groups'])['Total Price'].mean().round(2)
        grop_by_creditB = df_B.groupby(df_B['Credit Groups'])['Total Price'].mean().round(2)
        revenueA_B_Crediwise = self.merge_profit_series_in_dataframe(grop_by_creditA, grop_by_creditB, "credit groups",
                                                                     'revenue')

        group_by_vehicle_valueA = df_A.groupby(df_A['Vehiclevalue Groups'])['Total Price'].mean().round(2)
        group_by_vehicle_valueB = df_B.groupby(df_B['Vehiclevalue Groups'])['Total Price'].mean().round(2)
        revenue_A_B_vv = self.merge_profit_series_in_dataframe(group_by_vehicle_valueA, group_by_vehicle_valueB,
                                                               "vehicle value", 'revenue')

        group_by_vehicle_valueA = df_A.groupby(df_A['Mileage Groups'])['Total Price'].mean().round(2)
        group_by_vehicle_valueB = df_B.groupby(df_B['Mileage Groups'])['Total Price'].mean().round(2)
        revenue_A_B_vehicle_mile = self.merge_profit_series_in_dataframe(group_by_vehicle_valueA,
                                                                         group_by_vehicle_valueB, "mileage", 'revenue')

        group_by_licence_A = df_A.groupby(df_A['Licence Groups'])['Total Price'].mean().round(2)
        group_by_licence_B = df_B.groupby(df_B['Licence Groups'])['Total Price'].mean().round(2)
        revenue_A_B_licence = self.merge_profit_series_in_dataframe(group_by_licence_A, group_by_licence_B,
                                                                    "licence length", 'revenue')

        return revenueA_B_monthly, revenueA_B_weekly, revenue_A_B_agewise, revenueA_B_Crediwise, \
               revenue_A_B_vv, revenue_A_B_vehicle_mile, revenue_A_B_licence

    def get_gross_profit_for_chart(self, df_A, df_B):
        group_by_monthly_total_priceA = df_A.groupby(df_A['months'])['Gross Profit'].mean().round(2)
        group_by_monthly_total_priceA = self.oreder_series_months(group_by_monthly_total_priceA)
        group_by_monthly_total_priceB = df_B.groupby(df_B['months'])['Gross Profit'].mean().round(2)
        group_by_monthly_total_priceB = self.oreder_series_months(group_by_monthly_total_priceB)

        group_by_weekly_total_priceA = df_A.groupby(df_A['weeks'])['Gross Profit'].mean().round(2)
        group_by_weekly_total_priceB = df_B.groupby(df_B['weeks'])['Gross Profit'].mean().round(2)

        gross_profitA_B_monthly = self.merge_profit_series_in_dataframe(group_by_monthly_total_priceA,
                                                                        group_by_monthly_total_priceB, 'months',
                                                                        'gross profit')
        gross_profitA_B_weekly = self.merge_profit_series_in_dataframe(group_by_weekly_total_priceA,
                                                                       group_by_weekly_total_priceB, 'weeks',
                                                                       'gross profit')

        grop_by_ageA = df_A.groupby(df_A['Age Groups'])['Gross Profit'].mean().round(2)
        grop_by_ageB = df_B.groupby(df_B['Age Groups'])['Gross Profit'].mean().round(2)
        gross_profit_A_B_agewise = self.merge_profit_series_in_dataframe(grop_by_ageA, grop_by_ageB, "age groups",
                                                                         'gross profit')

        grop_by_creditA = df_A.groupby(df_A['Credit Groups'])['Gross Profit'].mean().round(2)
        grop_by_creditB = df_B.groupby(df_B['Credit Groups'])['Gross Profit'].mean().round(2)
        gross_profitA_B_Crediwise = self.merge_profit_series_in_dataframe(grop_by_creditA, grop_by_creditB,
                                                                          "credit groups",
                                                                          'gross profit')

        group_by_vehicle_valueA = df_A.groupby(df_A['Vehiclevalue Groups'])['Gross Profit'].mean().round(2)
        group_by_vehicle_valueB = df_B.groupby(df_B['Vehiclevalue Groups'])['Gross Profit'].mean().round(2)
        gross_profit_A_B_vv = self.merge_profit_series_in_dataframe(group_by_vehicle_valueA, group_by_vehicle_valueB,
                                                                    "vehicle value", 'gross profit')

        group_by_vehicle_valueA = df_A.groupby(df_A['Mileage Groups'])['Gross Profit'].mean().round(2)
        group_by_vehicle_valueB = df_B.groupby(df_B['Mileage Groups'])['Gross Profit'].mean().round(2)
        gross_profit_A_B_vehicle_mile = self.merge_profit_series_in_dataframe(group_by_vehicle_valueA,
                                                                              group_by_vehicle_valueB, "mileage",
                                                                              'gross profit')

        group_by_licence_A = df_A.groupby(df_A['Licence Groups'])['Gross Profit'].mean().round(2)
        group_by_licence_B = df_B.groupby(df_B['Licence Groups'])['Gross Profit'].mean().round(2)
        gross_profit_A_B_licence = self.merge_profit_series_in_dataframe(group_by_licence_A, group_by_licence_B,
                                                                         "licence length", 'gross profit')
        return gross_profitA_B_monthly, gross_profitA_B_weekly, gross_profit_A_B_agewise, \
               gross_profitA_B_Crediwise, gross_profit_A_B_vv, gross_profit_A_B_vehicle_mile, gross_profit_A_B_licence

    def get_revenue_AvsB(self, rev_A, rev_B, total):
        p1 = (rev_A * 100) / total
        p2 = (rev_B * 100) / total
        df = pd.DataFrame({"rev_percent": p1, "group": "A"}, index=[0])
        df2 = pd.DataFrame({"rev_percent": p2, "group": "B"}, index=[0])
        return pd.concat([df, df2])
