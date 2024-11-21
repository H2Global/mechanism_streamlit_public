# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 14:37:58 2024

@author: JulianReul
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

import pymechanism as pm
import plotly.graph_objects as go
#%%

def show_info_page():
    st.image("images/logo_H2G.png")
    st.header('Exploring the H2Global Mechanism')
        
    st.markdown("""
**How does the H2Global instrument work?**
                
\nH2Global accelerates clean hydrogen market creation through a pioneering double-auction mechanism combined with an intermediary—Hintco—that enters contracts with sellers and buyers that often struggle to connect independently at an early stage of market development. This intermediary then buys products—which are typically more expensive than their carbon-intensive counterparts—to sell them through an auction at a lower price to end consumers supporting demand build up. The price difference is covered by public funding though conceivably it could also be covered by climate funds, private capital, or a combination thereof. In so doing, the H2Global mechanism simulates a functioning market for clean hydrogen, helping shift market creation forward.

\nThe H2Global mechanism is the closest analog to a global market maker. It is unique in that it:

1. covers the whole value chain, from production to consumption.
2. provides continuous price discovery on the producers’ and consumers’ side.
3. provides flexibility to offtakers—made up of companies from hard-to-abate sectors like chemicals and steel—by ensuring access to large volumes of product, enhancing regulatory certainty through standardization of the contracts, and compensating costs until cleaner energy becomes more competitive.
4. promotes liquidity and encourages the emergence of secondary markets by using standardised short-term offtake contracts (1 year).
5. allows for swift responses to market changes by offering short-term offtake contracts.
6. provides bankability to producers by offering long-term purchase contracts (10 years) at a fixed price, reducing uncertainty.
7. reduces barriers to entry, promotes fair market pricing and efficient allocation of resources by operating a "double-auction scheme," where competitive auctions are held for both the supply and demand side.
8. ensures most efficient use of available (and often limited) funds for maximum impact, as it allows any increase in demand or changes in prices to be quickly incorporated.
9. mitigates the risk of financing stranded assets by only accessing public funding upon physical delivery of the products.
                
Exporters and importers of clean hydrogen and other similar products can all make use of H2Global’s mechanism. It is a flexible instrument that can empower governments to shape the global market for these products through customized funding windows. In general, individual funding windows can be defined in terms of geography, contract duration, product selection, and sustainability criteria. Whoever provides the funds for the compensation payments determines the design, specifications, and objectives of the respective funding window, ensuring that they are in line with their respective targets such as energy security, industrial competitiveness, etc. Funding windows can be deployed by a single country (import/export window or domestic window), by two countries (joint import/export window), or more (multilateral window), depending on the participating governments’ objectives.
                """)
    
    st.image("images/mechanism.png")


def show_evaluation_page():
    st.image("images/logo_H2G.png")
    st.title('Exploring the H2Global Mechanism')
    
    #Main input parameters    
    Derivative = st.selectbox(
    "Please select an energy carrier",
    ("Hydrogen", "Ammonia", "Sustainable Aviation Fuel (SAF)", "Methanol"),
    index=None,
    placeholder="Select energy carrier...",
    )
    
    Subsidy_Volume = st.number_input(
        'Funding volume [Billion US$]',
        value = 1.0,
        step=0.1,
        min_value=0.0
        )
    Subsidy_Volume = Subsidy_Volume*1e9

    Period = st.number_input(
        'Funding period [years]',
        value = 10,
        min_value=0
        )
    
    if Derivative == "Hydrogen":
        Purchase_Price_Start_DEFAULT = 6.0
        Purchase_Price_End_DEFAULT = 6.0
        Sales_Price_Start_DEFAULT = 3.0
        Sales_Price_End_DEFAULT = 4.5
    elif Derivative == "Ammonia":
        Purchase_Price_Start_DEFAULT = 1.0
        Purchase_Price_End_DEFAULT = 1.0
        Sales_Price_Start_DEFAULT = 0.5
        Sales_Price_End_DEFAULT = 0.65
    else:
        Purchase_Price_Start_DEFAULT = 6.0
        Purchase_Price_End_DEFAULT = 6.0
        Sales_Price_Start_DEFAULT = 3.0
        Sales_Price_End_DEFAULT = 4.5


    Purchase_Price_Start = st.number_input(
        'Purchase price start [US$/kg]',
        value = Purchase_Price_Start_DEFAULT,
        step=0.1,
        min_value=0.0,
        help="""The purchase price includes transport costs from the production site to the agreed demand location."""
        )
    Purchase_Price_End = st.number_input(
        'Purchase price end [US$/kg]',
        value = Purchase_Price_End_DEFAULT,
        step=0.1,
        min_value=0.0,
        help="""The purchase price includes transport costs from the production site to the agreed demand location."""
        )
    Sales_Price_Start = st.number_input(
        'Sales price start [US$/kg]',
        value = Sales_Price_Start_DEFAULT,
        step=0.1,
        min_value=0.0
        )

    Sales_Price_End = st.number_input(
        'Sales price end [US$/kg]',
        value = Sales_Price_End_DEFAULT,
        step=0.1,
        min_value=0.0
        )

    Sales_Price_Volatility = st.number_input(
        'Standard deviation of sales price [%] - BETA',
        value=0.0,
        step=0.5,
        min_value=0.0,
        max_value=20.0
    )

    Sales_Price_Volatility = Sales_Price_Volatility/100

    # Create an expander object
    expander_mechanism = st.expander("Click for further specifications of the H2Global mechanism")
    
    # Add content to the expander
    with expander_mechanism:
              
        #Ratio of the funding volume which is used to purchase hydrogen-derivatives for long-term SALES agreements.
        RATIO_LONGTERM_HSA = st.number_input(
            'Ratio of long-term sales agreements',
            value = 0.0,
            step=0.1,
            min_value=0.0,
            max_value=1.0,
            help="""The ratio of sales agreements covering the entire funding period. In the current tenders (as of early 2024), all sales agreements are short-term (1y)."""
            )
          
        #Ratio of the funding volume which is used to purchase hydrogen-derivatives for long-term SALES agreements.
        FLOOR_PRICE_HSA = st.number_input(
            'Floor price for long-term sales [US$/kg]',
            value = 4.0,
            step=0.1,
            min_value=0.0,
            help="""Only relevant, if long-term sales agreements exist. The floor price indicates the minimum price the offtaker is paying, even if the market price is lower than the floor price."""
            )
         
        #Ratio of the funding volume which is used to purchase hydrogen-derivatives for long-term SALES agreements.
        BID_CAP_HSA = st.number_input(
            'Ceiling price of long-term sales [US$/kg]',
            value = 4.0,
            step=0.1,
            min_value=0.0,
            help="""Only relevant, if long-term sales agreements exist. The ceiling price indicates the maximum price the offtaker is paying, even if the market price exceeds the ceiling price."""
            )
        
        #Keyword / specific input parameters
        Reinvest_Cycles = st.number_input(
            'Re-usage of sales revenue: cycles',
            value = 2,
            min_value=-1,
            help="""How often are the proceeds from sales being re-used for additional purchases per year?"""
            )
        
        #Ratio of the funding volume which is used to purchase hydrogen-derivatives for long-term SALES agreements.
        RATIO_GUARANTEED_SHORTTERM_HSA = st.number_input(
            'Ratio of guaranteed short-term sales',
            value = 0.0,
            step=0.1,
            min_value=0.0,
            max_value=1.0,
            help="""Short-term sales (1y) as a share of annual long-term purchases, which are guaranteed by a government entity in case no offtaker can be found."""
            )
    
    # Create an expander object
    expander_fiscal_benefits = st.expander("Click for further specifications of fiscal benefits")
    
    # Add content to the expander
    with expander_fiscal_benefits:
            
        #NOTE: Only consider additional fiscal benefits, 
        #which would not have been there without the subsidy.
        
        #Depreciation period of fiscal loan
        DEPRECIATION_PERIOD = st.number_input(
            'Depreciation period [years]',
            value = 25,
            step=1,
            min_value=0,
            )

        #Depreciation period of fiscal loan
        GRACE_PERIOD = st.number_input(
            'Grace period of the loan [years]',
            value = 8,
            step=1,
            min_value=0,
            help="During the grace period, no principal payments have to be made."
            )


        #Depreciation period of fiscal loan
        WACC_PERCENT = st.number_input(
            'Cost of Capital [%]',
            value = 2.5,
            step=0.1,
            min_value=0.0,
            )
        WACC = WACC_PERCENT/100

        #Depreciation period of fiscal loan
        INFLATION_PERCENT = st.number_input(
            'Inflation [%]',
            value = 3.0,
            step=0.1,
            min_value=0.0,
            )
        INFLATION = INFLATION_PERCENT/100

        #Income tax
        #____Only consider corporate tax on revenue of production projects.
        CORPORATE_TAX_RATE_PERCENT = st.number_input(
            'Corporate tax rate [%]',
            value = 35,
            step=1,
            min_value=0,
            )
        CORPORATE_TAX_RATE = CORPORATE_TAX_RATE_PERCENT / 100

        #VAT
        #____Consider this for:
        #____1) Investment costs on supply and demand side.
        #____2) HPA sales to Hintco
        #____3) HSA sales to final offtaker
        #____4) Final product: Direct reduced iron (DRI)
        #____5) Final product: Fertilizer
        #____6) VAT on domestically sold hydrogen or ammonia
        VAT_RATE_PERCENT = st.number_input(
            'VAT rate [%]',
            value = 19.0,
            step=1.0,
            min_value=0.0,
            )
        VAT_RATE = VAT_RATE_PERCENT / 100
        
        st.markdown("**Please specify below for which revenue streams VAT applies.**")

        VAT_INVEST_BOOL=st.checkbox(label="Investments into machinery and equipment")
        VAT_HPA_BOOL=st.checkbox(label="Revenue from HPA agreement")
        VAT_HSA_BOOL=st.checkbox(label="Revenue from HSA agreement")
        VAT_HYDROGEN_PRODUCT_BOOL=st.checkbox(label="Revenue from domestic hydrogen product (gaseous hydrogen or ammonia) sales")        
        if Derivative == "Hydrogen":
            VAT_DRI_BOOL=st.checkbox(label="Revenue from domestic DRI sales")
            VAT_FERTILIZER_BOOL = False
        if Derivative == "Ammonia":
            VAT_FERTILIZER_BOOL=st.checkbox(label="Revenue from domestic fertilizer sales")
            VAT_DRI_BOOL = False

        #Import duties
        IMPORT_DUTIES_RATE_PERCENT = st.number_input(
            'Import duties [%]',
            value = 0.0,
            step=1.0,
            min_value=0.0,
            )
        IMPORT_DUTIES_RATE = IMPORT_DUTIES_RATE_PERCENT / 100

        SHARE_IMPORTED_PRODUCTION_EQUIPMENT_PERCENT = st.number_input(
            'Share of the production equipment which is imported [%]',
            value = 90,
            step = 1,
            min_value=0,
            max_value=100,
            help="E.g. electrolyser imported from other country."
            )
        SHARE_IMPORTED_PRODUCTION_EQUIPMENT = SHARE_IMPORTED_PRODUCTION_EQUIPMENT_PERCENT/100


        #SHARES
        SHARE_HPA_CONTRACT_PERCENT = st.number_input(
            'Share of the HPA contract of total production [%]',
            value = 20,
            step=1,
            min_value=0,
            max_value=100
            )
        SHARE_HPA_CONTRACT_SINGLE = SHARE_HPA_CONTRACT_PERCENT/100
        
        RAMP_UP = st.number_input(
            'Ramp up period for production project [years]',
            value = 3,
            step=1,
            min_value=0,
            max_value=Period,
            help="During this period, the share of the HPA contract of the total production of the project decreases linearly from 1 to the indicated share."
            )
        
        if RAMP_UP > 0:
            DELTA_YEARS_RAMP_UP = DEPRECIATION_PERIOD - RAMP_UP
            SHARE_HPA_CONTRACT_RAMP_UP = np.linspace(1,SHARE_HPA_CONTRACT_SINGLE,RAMP_UP)
            SHARE_HPA_CONTRACT_AFTER_RAMP_UP = np.linspace(SHARE_HPA_CONTRACT_SINGLE,SHARE_HPA_CONTRACT_SINGLE,DELTA_YEARS_RAMP_UP)
            SHARE_HPA_CONTRACT = np.concatenate((SHARE_HPA_CONTRACT_RAMP_UP, SHARE_HPA_CONTRACT_AFTER_RAMP_UP))
        else:
            SHARE_HPA_CONTRACT = np.linspace(SHARE_HPA_CONTRACT_SINGLE,SHARE_HPA_CONTRACT_SINGLE,DEPRECIATION_PERIOD)
        
        SHARE_TAXABLE_INCOME_PERCENT = st.number_input(
            'Share of taxable income of total revenue of the production project [%]',
            value = 50,
            step=1,
            min_value=0,
            max_value=100
            )
        SHARE_TAXABLE_INCOME = SHARE_TAXABLE_INCOME_PERCENT/100
        
        SHARE_DOMESTIC_SALES_PERCENT = st.number_input(
            'Share of total hydrogen product which is sold domestically [%]',
            value = 50,
            step = 1,
            min_value=0,
            max_value=100
            )
        SHARE_DOMESTIC_SALES = SHARE_DOMESTIC_SALES_PERCENT/100
        
        if Derivative == "Hydrogen":
            SHARE_H2_DRI_DOMESTIC_PERCENT = st.number_input(
                'Share of hydrogen which is used for the domestic production of DRI [%]',
                value = 50,
                step = 1,
                min_value=0,
                max_value=100,
                )
            SHARE_H2_DRI_DOMESTIC = SHARE_H2_DRI_DOMESTIC_PERCENT/100

            DRI_SALES_PRICE_PER_TON = st.number_input(
                'Domestic sales price of DRI [USD/ton]',
                value = 300,
                step = 10,
                min_value=0,
                )
            DRI_SALES_PRICE = DRI_SALES_PRICE_PER_TON/1000
    
            DRI_PER_KG_H2 = st.number_input(
                'DRI production per consumed hydrogen [kg-DRI/kg-H2]',
                value = 20,
                step = 1,
                min_value=0,
                )
    
            SHARE_DOMESTIC_SALES_DRI_PERCENT = st.number_input(
                'Share of DRI which is sold domestically [%]',
                value = 100,
                step = 1,
                min_value=0,
                )
            SHARE_DOMESTIC_SALES_DRI = SHARE_DOMESTIC_SALES_DRI_PERCENT/100
        
            #DEFINE FOR FUNCTIONALITY
            SHARE_NH3_FERTILIZER_DOMESTIC = 0
            FERTILIZER_SALES_PRICE = 0
            FERTILIZER_PER_KG_NH3 = 2
            SHARE_DOMESTIC_SALES_FERTILIZER = 0

        if Derivative == "Ammonia":

            SHARE_NH3_FERTILIZER_DOMESTIC_PERCENT = st.number_input(
                'Share of ammonia which is used for the domestic production of fertilizer [%]',
                value = 50,
                step = 1,
                min_value=0,
                )
            SHARE_NH3_FERTILIZER_DOMESTIC = SHARE_NH3_FERTILIZER_DOMESTIC_PERCENT/100
    
            FERTILIZER_SALES_PRICE_PER_TON = st.number_input(
                'Domestic sales price of ammonia-based fertilizer [USD/ton]',
                value = 500,
                step = 10,
                min_value=0,
                )
            FERTILIZER_SALES_PRICE = FERTILIZER_SALES_PRICE_PER_TON/1000
    
            FERTILIZER_PER_KG_NH3 = st.number_input(
                'Fertilizer (urea) production per consumed ammonia [kg-fertilizer/kg-NH3]',
                value = 2.0,
                step = 0.1,
                min_value=0.0,
                )
    
            SHARE_DOMESTIC_SALES_FERTILIZER_PERCENT = st.number_input(
                'Share of fertilizer which is sold domestically [%]',
                value = 100,
                step = 1,
                min_value=0,
                )
            SHARE_DOMESTIC_SALES_FERTILIZER = SHARE_DOMESTIC_SALES_FERTILIZER_PERCENT/100
                
            #DEFINE FOR FUNCTIONALITY
            SHARE_H2_DRI_DOMESTIC = 0
            DRI_SALES_PRICE = 0
            DRI_PER_KG_H2 = 20
            SHARE_DOMESTIC_SALES_DRI = 0
        
    
    st.markdown("**Which metrics do you want to visualize?**")
    
    VIS_0=st.checkbox(label="Traded energy [US$]")
    VIS_1=st.checkbox(label="Traded energy [tons]")
    VIS_2_A=st.checkbox(label="Annual funding spent [US$]")
    VIS_2_B=st.checkbox(label="Total funding spent [US$]")
    VIS_3=st.checkbox(label="Mitigated CO2-emissions [tons]")
    VIS_4=st.checkbox(label="Required electrolyzer capacity [GW]")
    VIS_5=st.checkbox(label="Visualize net-present value of fiscal benefits to the state [US$]")
    VIS_6=st.checkbox(label="Visualize absolute fiscal cashflows [US$]")
    
    
    if st.button("Confirm selection"):   
    
        if Sales_Price_End >= Purchase_Price_End and (RATIO_GUARANTEED_SHORTTERM_HSA > 0 or Reinvest_Cycles == -1):
            raise ValueError("Definition of input parameters leads to infinite energy purchases. Consider a sales price below the purchase price.")
        
        purchase_price_array = np.linspace(Purchase_Price_Start, Purchase_Price_End, Period)
        sales_price_array = np.linspace(Sales_Price_Start, Sales_Price_End, Period)
        
        #(NEW - USING PyPI Package)
        mechanism_instance = pm.Mechanism(
            purchase_price=purchase_price_array,
            sales_price=sales_price_array,
            subsidy_period=Period,
            subsidy_volume=Subsidy_Volume,
            RATIO_LONGTERM_HSA=RATIO_LONGTERM_HSA,
            FLOOR_PRICE_HSA=FLOOR_PRICE_HSA,
            BID_CAP_HSA=BID_CAP_HSA,
            REINVEST_CYCLES=Reinvest_Cycles,
            RATIO_GUARANTEED_SHORTTERM_HSA=RATIO_GUARANTEED_SHORTTERM_HSA,
            VOLATILITY=Sales_Price_Volatility
            )
        
        #simulate mechanism
        mechanism_instance.simulate_mechanism()
            
        #Plot hydrogen purchases
        data_to_plot = pd.DataFrame(
            {
               "Hydrogen Purchases [kg]": mechanism_instance.ATTR["Yearly_Product_Purchases"].mean(axis=1),
               "Hydrogen Purchases STD [kg]": mechanism_instance.ATTR["Yearly_Product_Purchases"].std(axis=1),
               "Hydrogen Purchases from Funding [$]": mechanism_instance.ATTR["Yearly_Purchases_LONG"].mean(axis=1),
               "Hydrogen Purchases from Funding STD [$]": mechanism_instance.ATTR["Yearly_Purchases_LONG"].std(axis=1),
               "Hydrogen Purchases from Sales Revenue [$]": mechanism_instance.ATTR["Yearly_Purchases_SHORT"].mean(axis=1),
               "Hydrogen Purchases from Sales Revenue STD [$]": mechanism_instance.ATTR["Yearly_Purchases_SHORT"].std(axis=1),
               "Used Funding Volume [$]": mechanism_instance.ATTR["Yearly_Used_Funding"].mean(axis=1),
               "Used Funding Volume STD [$]": mechanism_instance.ATTR["Yearly_Used_Funding"].std(axis=1),
               "Annual Sales [$]" : mechanism_instance.ATTR["Yearly_Sales"].mean(axis=1),
               "Annual Sales STD [$]" : mechanism_instance.ATTR["Yearly_Sales"].std(axis=1)
               }
            )
        
        data_to_plot["Year"] = range(1,Period+1)
        #Derive purchased hydrogen quantities in kg and tons
        data_to_plot["Hydrogen Purchases [$]"] = data_to_plot["Hydrogen Purchases from Funding [$]"] + data_to_plot["Hydrogen Purchases from Sales Revenue [$]"]
        data_to_plot["Hydrogen Purchases STD [$]"] = data_to_plot["Hydrogen Purchases from Funding STD [$]"] + data_to_plot["Hydrogen Purchases from Sales Revenue STD [$]"]
        data_to_plot["Hydrogen Purchases [tons]"] = data_to_plot["Hydrogen Purchases [kg]"] / 1000
        data_to_plot["Hydrogen Purchases STD [tons]"] = data_to_plot["Hydrogen Purchases STD [kg]"] / 1000
        data_to_plot["Hydrogen Purchases from Funding [kg]"] = mechanism_instance.ATTR["Yearly_Product_Purchases_LONG"].mean(axis=1)
        data_to_plot["Hydrogen Purchases from Funding [tons]"] = data_to_plot["Hydrogen Purchases from Funding [kg]"] / 1000
        data_to_plot["Hydrogen Purchases from Sales Revenue [kg]"] = data_to_plot["Hydrogen Purchases [kg]"] - data_to_plot["Hydrogen Purchases from Funding [kg]"]
        data_to_plot["Hydrogen Purchases from Sales Revenue [tons]"] = data_to_plot["Hydrogen Purchases from Sales Revenue [kg]"] / 1000
        data_to_plot["NOT Used Funding Volume [$]"] = Subsidy_Volume/Period - data_to_plot["Used Funding Volume [$]"]
        data_to_plot["Total Used Funding Volume [$]"] = data_to_plot["Used Funding Volume [$]"].cumsum()
        data_to_plot["Total NOT Used Funding Volume [$]"] = Subsidy_Volume - data_to_plot["Total Used Funding Volume [$]"]
        
        #Efficiency from renewable electricity to 
        dict_efficiency_factors = {
            "Hydrogen" : 0.7,
            "Ammonia" : 0.7*0.55,
            "Sustainable Aviation Fuel (SAF)" : 0.7*0.6,
            "Methanol" : 0.7*0.8
            }
        
        #Lower heating values
        dict_LHV = {
            "Hydrogen" : 33.33,
            "Ammonia" : 5.2,
            "Sustainable Aviation Fuel (SAF)" : 12.17,
            "Methanol" : 5.58
            }
    
        
        #operational full load hours of the electrolyzer
        full_load_hours = 4000
        data_to_plot["Required installed electrolyzer capacity [GW]"] = data_to_plot["Hydrogen Purchases [tons]"]*1e+3*dict_LHV[Derivative]*1e-6 / (full_load_hours*dict_efficiency_factors[Derivative])
        
        #VISUALIZATIONS
        
        #____Define short name for derivative
        if Derivative == "Hydrogen":
            Derivative_Short = "Hydrogen"
        elif Derivative == "Ammonia":
            Derivative_Short = "Ammonia"
        elif Derivative == "Sustainable Aviation Fuel (SAF)":
            Derivative_Short = "SAF"
        elif Derivative == "Methanol":
            Derivative_Short = "Methanol"
        else:
            raise ValueError("No such carrier defined.")
        
        if VIS_0:
                    
            fig = go.Figure()
            
            #Add bar for Hydrogen Purchases from Funding with error bars
            fig.add_trace(go.Bar(
                x=data_to_plot['Year'],
                y=data_to_plot['Hydrogen Purchases from Funding [$]'],
                name=Derivative_Short + ' purchases <br>using initial funding [US$]'
                )
            )
    
            # Add bar for Hydrogen Purchases from Sales Revenue with error bars
            fig.add_trace(go.Bar(
                x=data_to_plot['Year'],
                y=data_to_plot['Hydrogen Purchases from Sales Revenue [$]'],
                name=Derivative_Short + ' purchases <br>using sales revenue [US$]',
                error_y=dict(
                    type='data',
                    array=data_to_plot["Hydrogen Purchases STD [$]"],
                    visible=True)
                ),
                )
    
            # Update layout to stack bars
            fig.update_layout(
                title="Traded " + Derivative_Short + " [US$]",
                barmode='stack',  # Stack bars
                xaxis_title='Year',
                yaxis_title='Cashflows [US$]',
            )
            
            # Render the Plotly chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)
            
            Total_Hydrogen_Purchases = data_to_plot["Hydrogen Purchases [$]"].sum() * 1e-6
            
            st.write("Total ", Derivative_Short, " purchases within contract period [Million $]:", int(round(Total_Hydrogen_Purchases, 0)))
          
        if VIS_1:
            
            
            fig1 = go.Figure()
            
            #Add bar for Hydrogen Purchases from Funding with error bars
            fig1.add_trace(go.Bar(
                x=data_to_plot['Year'],
                y=data_to_plot['Hydrogen Purchases from Funding [tons]'],
                name=Derivative_Short + ' purchases <br>using initial funding [tons]'
                )
            )
    
            # Add bar for Hydrogen Purchases from Sales Revenue with error bars
            fig1.add_trace(go.Bar(
                x=data_to_plot['Year'],
                y=data_to_plot['Hydrogen Purchases from Sales Revenue [tons]'],
                name=Derivative_Short + ' purchases <br>using sales revenue [tons]',
                error_y=dict(
                    type='data',
                    array=data_to_plot["Hydrogen Purchases STD [tons]"],
                    visible=True)
                ),
                )
    
            # Update layout to stack bars
            fig1.update_layout(
                title="Traded " + Derivative_Short + " [tons]",
                barmode='stack',  # Stack bars
                xaxis_title='Year',
                yaxis_title="Purchased " + Derivative_Short + " [tons]",
            )
            
            # Render the Plotly chart in Streamlit
            st.plotly_chart(fig1, use_container_width=True)
        
            Total_Hydrogen_Quantity = (
                data_to_plot["Hydrogen Purchases from Funding [tons]"] +
                data_to_plot["Hydrogen Purchases from Sales Revenue [tons]"]
                ).sum()
                    
            st.write("Total purchased ", Derivative_Short," [Mt]:", round(Total_Hydrogen_Quantity*1e-6, 2))
    
        if VIS_2_A:
            
            fig2a = px.bar(
                data_to_plot, 
                x='Year', 
                y=[
                    "Used Funding Volume [$]", 
                    "NOT Used Funding Volume [$]",
                    ],
                title="Annual Funding Usage",
                labels={ # replaces default labels by column name
                        "value": "Annual funding [US$]",
                    },
                color_discrete_map={'Used Funding Volume [$]': 'rgb(204, 85, 0)', 'NOT Used Funding Volume [$]': 'rgb(255, 165, 0)'}
                )
            
            fig2a.update_traces(
                name='Funding spent [US$]',
                selector=dict(name='Used Funding Volume [$]')
            )     
            
            fig2a.update_traces(
                name='Funding remaining [US$]',
                selector=dict(name='NOT Used Funding Volume [$]')
            )     
            
            #NOT Used Funding Volume --> Remaining funding
            st.plotly_chart(fig2a, use_container_width=True)
            
            Total_Used_Funding = data_to_plot["Used Funding Volume [$]"].sum()
            Total_NOT_Used_Funding = data_to_plot["NOT Used Funding Volume [$]"].sum()
            RATIO_FUNDING_UTILIZATION = int((Total_Used_Funding / Subsidy_Volume)*100)
            
            st.write("Ratio of funding used:", RATIO_FUNDING_UTILIZATION, "[%]")
            st.write("Total amount of funding used:", int(round(Total_Used_Funding * 1e-6, 0)), "[Million US$]")
            
        if VIS_2_B:
            
            fig2b = px.bar(
                data_to_plot, 
                x='Year', 
                y=[
                    "Total Used Funding Volume [$]", 
                    "Total NOT Used Funding Volume [$]",
                    ],
                title="Total Funding Usage",
                labels={ # replaces default labels by column name
                        "value": "Total funding volume [US$]",
                    },
                color_discrete_map={"Total Used Funding Volume [$]": 'rgb(204, 85, 0)', "Total NOT Used Funding Volume [$]": 'rgb(255, 165, 0)'}
                )
            
            fig2b.update_traces(
                name='Total funding spent [US$]',
                selector=dict(name='Total Used Funding Volume [$]')
            )     
            
            fig2b.update_traces(
                name='Total funding remaining [US$]',
                selector=dict(name='Total NOT Used Funding Volume [$]')
            )     
            
            st.plotly_chart(fig2b, use_container_width=True)
            
            Total_Used_Funding = data_to_plot["Used Funding Volume [$]"].sum()
            Total_NOT_Used_Funding = data_to_plot["NOT Used Funding Volume [$]"].sum()
            RATIO_FUNDING_UTILIZATION = int((Total_Used_Funding / Subsidy_Volume)*100)
            
            st.write("Ratio of funding used:", RATIO_FUNDING_UTILIZATION, "[%]")
            st.write("Total amount of funding used:", int(round(Total_Used_Funding * 1e-6, 0)), "[Million US$]")
               
        if VIS_3:
            #Plot mitigated CO2 emissions
            #____Emissions according to EU commission: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv%3AOJ.L_.2023.157.01.0020.01.ENG&toc=OJ%3AL%3A2023%3A157%3ATOC
            #________Grey Methanol: 97.1 gCO2eq/MJ, LHV: 19.9 MJ/kg --> 1932.3 gCO2eq/kg
            #________Grey Ammonia: 2351.3 gCO2eq/kg, LHV: 18.8 MJ/kg --> 2351.3 gCO2eq/kg
            #________Grey Kerosene: --> 3150 gCO2/kgSAF
            #____Reference: RED II --> Green hydrogen must mitigate CO2-emissions by a min. of 3.38 kg_CO2/kg_H2
            #____Reference: Buberger et al. (2022)
    
            dict_emission_reduction = {
                "Hydrogen" : 3.38,
                "Ammonia" : 2.351*0.7,
                "Sustainable Aviation Fuel (SAF)" : 3.15*0.7,
                "Methanol" : 1.932*0.7
                }
            
            data_to_plot["Mitigated CO2-emissions [tons]"] = data_to_plot["Hydrogen Purchases [tons]"]*dict_emission_reduction[Derivative]
        
            fig3 = px.scatter(
                data_to_plot, 
                x='Year', 
                y='Mitigated CO2-emissions [tons]',
                title="Mitigated CO2-emissions* [tons]"
                )
            fig3.update_traces(mode='lines+markers', line_shape='linear', marker_color='green')
            fig3.update_layout(width=600, height=500, yaxis=dict(range=[0, 1.1*max(data_to_plot['Mitigated CO2-emissions [tons]'])]))
            
            st.plotly_chart(fig3, use_container_width=True)
            
            st.markdown(
                """
                *in comparison to grey product.
                """
                )
            
            total_mitigated_co2 = data_to_plot["Mitigated CO2-emissions [tons]"].sum()
            total_mitigated_co2_million = total_mitigated_co2*1e-6
            total_car_equivalent = total_mitigated_co2 / 50
            
            st.write(
                "Total amount of reduced CO2-emissions compared to the grey product:", 
                round(total_mitigated_co2_million, 2), 
                "Mt. This amount equals the life-cycle emissions of", 
                int(total_car_equivalent), "cars."
                )
                    
            st.markdown("""
                        Assumptions: 
                            
                        1) Life-cycle emissions of a gasoline passenger car are ~50 tons CO2-eq. [6]
                        2) Reduced CO2-emissions of green product compared to grey product: 70% according to RED II [3]
                                                                                 """)
    
        if VIS_4:
    
            #Plot expected installed electrolysis capacity [GW]
            #____electrolyzer efficiency: 60% --> Reference [2]
            #____Full load hours: 4000 hours --> No reference yet!
            # H2 [GWh] = Installed capacity [GW] * FLH [h/a] * efficiency; 1000 ton H2 = 33.33 GWh H2 --> 1000/33.33 ton H2 = 30 ton H2 = 1 GWh H2 --> 1 ton H2 = 1/30 GWh H2
            # --> Installed capacity [GW] = H2 [GWh] / (FLH [h/a] * efficiency)
        
            fig4 = px.scatter(
                data_to_plot, 
                x='Year',
                y='Required installed electrolyzer capacity [GW]',
                title="Required Installed Electrolyzer Capacity for Green Hydrogen Production [GW]"
                )
            fig4.update_traces(mode='lines+markers', line_shape='linear', marker_color='green')
            fig4.update_layout(width=600, height=500, yaxis=dict(range=[0, 1.1*max(data_to_plot['Required installed electrolyzer capacity [GW]'])]))
            
            st.plotly_chart(fig4 , use_container_width=True)
            st.markdown("""
                        Technology Assumptions:
                            
                        1) Electrolyzer full-load hours: 4000 h [5]
                        2) Electrolyzer efficiency: 70% [4]
                                                                                 """)
        
        if VIS_5 or VIS_6:
            
            FISCAL_NPV, FISCAL_CASHFLOWS_DICT, LOAN_CASHFLOWS_DICT, SALES_REVENUES_DICT = get_fiscal_npv(
                    PRODUCT_TYPE=Derivative,
                    TOTAL_LOAN=Subsidy_Volume,
                    ANNUAL_PRODUCTION=data_to_plot["Hydrogen Purchases [kg]"], #kg
                    ANNUAL_PRODUCT_PURCHASES=data_to_plot["Hydrogen Purchases [$]"], #USD
                    ANNUAL_PRODUCT_SALES=data_to_plot["Annual Sales [$]"], #USD
                    ANNUAL_FUNDING=data_to_plot["Used Funding Volume [$]"], #USD   
                    DEPRECIATION_PERIOD=DEPRECIATION_PERIOD, #YEARS
                    GRACE_PERIOD=GRACE_PERIOD,
                    CONTRACT_PERIOD_HPA=Period,
                    WACC=WACC,
                    INFLATION=INFLATION,
                    CORPORATE_TAX_RATE=CORPORATE_TAX_RATE,
                    SHARE_HPA_CONTRACT=SHARE_HPA_CONTRACT, #This is the share that the HPA contract takes of the companies total revenue.
                    SHARE_TAXABLE_INCOME=SHARE_TAXABLE_INCOME, #This is the share of the taxable income of the total revenue of the supply side company.
                    SHARE_DOMESTIC_SALES=SHARE_DOMESTIC_SALES, #This is the share of the hydrogen product which is sold domestically.
                    SHARE_IMPORTED_PRODUCTION_EQUIPMENT=SHARE_IMPORTED_PRODUCTION_EQUIPMENT, #This is the share of imported production equipment required to construct the production plant.
                    SHARE_H2_DRI_DOMESTIC=SHARE_H2_DRI_DOMESTIC, #This is the share of the domestically sold hydrogen, which is used for domestic DRI production.  
                    DRI_SALES_PRICE=DRI_SALES_PRICE, #USD/kg
                    DRI_PER_KG_H2=DRI_PER_KG_H2, #DRI output per input of H2
                    SHARE_DOMESTIC_SALES_DRI=SHARE_DOMESTIC_SALES_DRI, #How much of the fertilizer is then sold domestically?
                    SHARE_NH3_FERTILIZER_DOMESTIC=SHARE_NH3_FERTILIZER_DOMESTIC, #This is the share of the domestically sold ammonia, which is used for domestic fertilizer production.  
                    FERTILIZER_SALES_PRICE=FERTILIZER_SALES_PRICE, #
                    FERTILIZER_PER_KG_NH3=FERTILIZER_PER_KG_NH3, #Fertilizer output per input of NH3
                    SHARE_DOMESTIC_SALES_FERTILIZER=SHARE_DOMESTIC_SALES_FERTILIZER, #How much of the fertilizer is then sold domestically?
                    IMPORT_DUTIES_RATE=IMPORT_DUTIES_RATE,
                    VAT_RATE=VAT_RATE,
                    VAT_INVEST_BOOL=VAT_INVEST_BOOL,
                    VAT_HPA_BOOL=VAT_HPA_BOOL,
                    VAT_HSA_BOOL=VAT_HSA_BOOL,
                    VAT_HYDROGEN_PRODUCT_BOOL=VAT_HYDROGEN_PRODUCT_BOOL,
                    VAT_DRI_BOOL=VAT_DRI_BOOL,
                    VAT_FERTILIZER_BOOL=VAT_FERTILIZER_BOOL
                    )
            
            if VIS_5:                                

                # Convert dictionary to calculate total depreciated cashflows for each category
                categories = list(FISCAL_CASHFLOWS_DICT.keys())
                FISCAL_CASHFLOWS_TOTAL_DEPRECIATED = {}
                
                for c in categories:
                    CASHFLOW_DEPRECIATED_TOTAL = 0
                    FISCAL_CASHFLOWS_TEMP = FISCAL_CASHFLOWS_DICT[c]
                    
                    # If the value is a scalar, add it directly; otherwise, depreciate it over the specified period and sum
                    if isinstance(FISCAL_CASHFLOWS_TEMP, (int, float)):
                        FISCAL_CASHFLOWS_TOTAL_DEPRECIATED[c] = FISCAL_CASHFLOWS_TEMP
                    else:
                        for t in range(DEPRECIATION_PERIOD):
                            CASHFLOW_DEPRECIATED_TOTAL += FISCAL_CASHFLOWS_TEMP[t] / (1 + WACC) ** t
                        FISCAL_CASHFLOWS_TOTAL_DEPRECIATED[c] = CASHFLOW_DEPRECIATED_TOTAL
                
                # Prepare data for Plotly as a single stacked bar
                data = [{'Category': category, 'Total Depreciated Cashflow': value} 
                        for category, value in FISCAL_CASHFLOWS_TOTAL_DEPRECIATED.items()]
                
                # Create a DataFrame for visualization
                df = pd.DataFrame(data)
                
                # Add a dummy column for y-axis to create a single stacked bar
                df['Stacked Bar'] = 'Total Depreciated Cashflow'
                
                # Create a single stacked bar chart
                fig5 = px.bar(
                    df,
                    x="Stacked Bar",  # Single stacked bar label
                    y="Total Depreciated Cashflow",
                    color="Category",
                    labels={'Total Depreciated Cashflow': 'Total Depreciated Cashflow [US$]', 'Stacked Bar': ''},
                    title="Total Depreciated Cashflow for All Categories [US$]",
                )
                
                # Customize the chart
                fig5.update_layout(
                    xaxis=dict(showticklabels=False),  # Hide x-axis tick label
                    yaxis=dict(
                        title="Total Depreciated Cashflow [US$]",
                        zeroline=True,          # Show a zero line on the y-axis
                        zerolinecolor="black",   # Set the color of the zero line
                        zerolinewidth=1.5        # Set the thickness of the zero line
                    ),
                    showlegend=True  # Show legend for categories
                )
                
                # Display the chart in Streamlit
                st.plotly_chart(fig5)
                
                # Display NPV calculation
                st.write(
                    "Net-present value of funding instrument for fiscal authority:", 
                    round(FISCAL_NPV * 1e-6, 2), 
                    "[Million US$]"
                )
                    
            if VIS_6:
                
                # Combine fiscal and loan cashflows into a DataFrame for each year
                years = list(range(1, DEPRECIATION_PERIOD + 1))  # Define years as labels
                data = {"Year": years}
                
                # Add fiscal cashflows to data dictionary
                for key, values in FISCAL_CASHFLOWS_DICT.items():
                    if key == "FISCAL_EXPENSES":
                        continue
                    else:
                        data[key] = values
                
                # Add loan cashflows to data dictionary
                for key, values in LOAN_CASHFLOWS_DICT.items():
                    data[key] = values
                
                # Convert data dictionary to a DataFrame
                df = pd.DataFrame(data)
                
                # Melt DataFrame for Plotly to create stacked bars
                df_melted = df.melt(id_vars=["Year"], var_name="Category", value_name="Cashflow")
                
                # Create a stacked bar chart in Plotly
                fig6 = px.bar(
                    df_melted,
                    x="Year",
                    y="Cashflow",
                    color="Category",
                    title="Yearly Cashflows by Category [US$]",
                    labels={"Cashflow": "Cashflow [US$]", "Year": "Year"},
                )
                
                # Customize the chart
                fig6.update_layout(
                    yaxis=dict(title="Cashflow [US$]", zeroline=True, zerolinecolor="black", zerolinewidth=1.5),
                    showlegend=True
                )
                
                
                # Display the chart in Streamlit
                st.plotly_chart(fig6)
            
                #Output of sales revenues
                TOTAL_DOMESTIC_REVENUES = SALES_REVENUES_DICT["DOMESTIC_SALES_REVENUE"].sum()
                st.write("Total domestic sales revenue (hydrogen product, fertilizer, DRI) [USD Mio.]:", round(TOTAL_DOMESTIC_REVENUES*1e-6, 1))
                TOTAL_EXPORT_REVENUES = SALES_REVENUES_DICT["EXPORT_SALES_REVENUE"].sum()
                st.write("Total export sales revenue (hydrogen product, fertilizer, DRI) [USD Mio.]:", round(TOTAL_EXPORT_REVENUES*1e-6, 1))

            
def get_fiscal_npv(
        PRODUCT_TYPE,
        TOTAL_LOAN,
        ANNUAL_PRODUCTION, #kg
        ANNUAL_PRODUCT_PURCHASES, #USD
        ANNUAL_PRODUCT_SALES, #USD
        ANNUAL_FUNDING, #USD
        DEPRECIATION_PERIOD, #YEARS
        GRACE_PERIOD, #YEARS
        CONTRACT_PERIOD_HPA, #years
        WACC,
        INFLATION,
        CORPORATE_TAX_RATE,
        SHARE_HPA_CONTRACT, #This is the share that the HPA contract takes of the companies total revenue.
        SHARE_TAXABLE_INCOME, #This is the share of the taxable income of the total revenue of the supply side company.
        SHARE_DOMESTIC_SALES, #This is the share of the hydrogen product which is sold domestically.
        SHARE_IMPORTED_PRODUCTION_EQUIPMENT, #This is the share of imported production equipment required to construct the production plant.
        SHARE_H2_DRI_DOMESTIC, #This is the share of the domestically sold hydrogen, which is used for domestic DRI production.  
        DRI_SALES_PRICE, #USD/kg
        DRI_PER_KG_H2, #DRI output per input of H2
        SHARE_DOMESTIC_SALES_DRI, #How much of the fertilizer is then sold domestically?
        SHARE_NH3_FERTILIZER_DOMESTIC, #This is the share of the domestically sold ammonia, which is used for domestic fertilizer production.  
        FERTILIZER_SALES_PRICE, #
        FERTILIZER_PER_KG_NH3, #Fertilizer output per input of NH3
        SHARE_DOMESTIC_SALES_FERTILIZER, #How much of the fertilizer is then sold domestically?
        IMPORT_DUTIES_RATE,
        VAT_RATE,
        VAT_INVEST_BOOL,
        VAT_HPA_BOOL,
        VAT_HSA_BOOL,
        VAT_HYDROGEN_PRODUCT_BOOL,
        VAT_DRI_BOOL,
        VAT_FERTILIZER_BOOL,
        ):
    
    if CONTRACT_PERIOD_HPA > DEPRECIATION_PERIOD:
        raise ValueError("Depreciation period of loan is shorter than HPA contract period.")
    else:
        if DEPRECIATION_PERIOD >= CONTRACT_PERIOD_HPA:
            delta_years = DEPRECIATION_PERIOD - CONTRACT_PERIOD_HPA
        else:
            raise ValueError("Loan period must be equal to or larger than contract period.")
        
        #resize external input arrays.
        #____This is the annual production volume under the HPA contract in kg
        ANNUAL_PRODUCTION = np.concatenate([ANNUAL_PRODUCTION, np.full(delta_years, ANNUAL_PRODUCTION.iloc[-1])]) #kg
        #____These are the annual product purchases by Hintco
        ANNUAL_PRODUCT_PURCHASES_HINTCO = np.concatenate([ANNUAL_PRODUCT_PURCHASES, np.zeros(delta_years)]) #USD
        #____This is for how much producers can sell to the market, after the offtake contract expired.
        #____Conservative assumption: Last Hintco sales price*inflation
        ANNUAL_PRODUCT_SALES_AFTER_HINTCO = np.array([ANNUAL_PRODUCT_SALES.iloc[-1]*(1+INFLATION)**t for t in range(delta_years)])
        #____These are the annual product purchases by Hintco, extended by a future offtake --> Used for calculating the revenue of the production projects.
        #____Assume the last Hintco sales price here and increase this by inflation.
        ANNUAL_PRODUCT_PURCHASES_TOTAL = np.concatenate([ANNUAL_PRODUCT_PURCHASES, ANNUAL_PRODUCT_SALES_AFTER_HINTCO]) #USD
        #____These are the sales via hintco within the contract period.
        ANNUAL_PRODUCT_SALES_HINTCO = np.concatenate([ANNUAL_PRODUCT_SALES, np.zeros(delta_years)]) #USD
        #____These are the sales by Hintco, extended by future offtake. --> Used for domestic and export volume calculations.
        #____Assume the last Hintco sales price here and increase this by inflation.
        ANNUAL_PRODUCT_SALES_TOTAL = np.concatenate([ANNUAL_PRODUCT_SALES, ANNUAL_PRODUCT_SALES_AFTER_HINTCO]) #USD
        #____This is the required funding for Hintco.
        ANNUAL_FUNDING_LONG = np.concatenate([ANNUAL_FUNDING, np.zeros(delta_years)]) #USD
        
    #Calculate fiscal benefits. (tax revenues)
    #____CORPORATE_TAX: Only include supply side, because these will be genuinely new businesses.
    TOTAL_ANNUAL_PRODUCTION = ANNUAL_PRODUCT_PURCHASES_TOTAL / SHARE_HPA_CONTRACT
    TOTAL_ANNUAL_PRODUCTION_KG = ANNUAL_PRODUCTION / SHARE_HPA_CONTRACT
    TOTAL_ANNUAL_PRODUCT_SALES = ANNUAL_PRODUCT_SALES_TOTAL / SHARE_HPA_CONTRACT
    TAXABLE_INCOME = (SHARE_HPA_CONTRACT*TOTAL_ANNUAL_PRODUCTION + (1-SHARE_HPA_CONTRACT)*TOTAL_ANNUAL_PRODUCT_SALES)*SHARE_TAXABLE_INCOME
    CORPORATE_TAX = TAXABLE_INCOME * CORPORATE_TAX_RATE
    DOMESTIC_SALES_REVENUE = 0
    EXPORT_SALES_REVENUE = 0
    
    #____VAT_RATE_INVEST: Includes the VAT on initial investments on the supply side.
    VAT_INVEST = np.zeros(DEPRECIATION_PERIOD)
    if PRODUCT_TYPE == "Ammonia":
        CAPEX_PER_KG_ANNUAL_PRODUCTION = 10 #Evaluation Kenya White Paper: 5.2 (Turkana South 500 MW), Turkana Central 10 MW: 10.6, Kisumu 10GW: 15.7 €/kg NH3/year
    elif PRODUCT_TYPE == "Hydrogen":
        CAPEX_PER_KG_ANNUAL_PRODUCTION = 45 #Evaluation Kenya White Paper: 22.3 (Turkana South 500 MW), Turkana Central 10 MW: 38.4, Kisumu 10GW: 57.5 €/kg H2/year 
    else:
        raise AttributeError("Unknown -PRODUCT_TYPE-")
        
    CAPEX = np.max(ANNUAL_PRODUCTION) * CAPEX_PER_KG_ANNUAL_PRODUCTION
    if VAT_INVEST_BOOL:
        VAT_INVEST[0] = CAPEX * VAT_RATE
    else:
        VAT_INVEST[0] = 0
    
    #____IMPORT_DUTIES_RATE
    IMPORT_DUTIES = np.zeros(DEPRECIATION_PERIOD)
    IMPORT_DUTIES[0] = CAPEX * SHARE_IMPORTED_PRODUCTION_EQUIPMENT * IMPORT_DUTIES_RATE
    
    #____VAT_HPA
    if VAT_HPA_BOOL:
        VAT_HPA = VAT_RATE * ANNUAL_PRODUCT_PURCHASES_HINTCO
    else:
        VAT_HPA = 0
    
    #____VAT_HSA
    if VAT_HSA_BOOL:
        VAT_HSA = VAT_RATE * ANNUAL_PRODUCT_SALES_HINTCO
    else:
        VAT_HSA = 0
        
    TOTAL_DOMESTIC_PRODUCTION = TOTAL_ANNUAL_PRODUCT_SALES * SHARE_DOMESTIC_SALES
    TOTAL_EXPORT_PRODUCTION = TOTAL_ANNUAL_PRODUCT_SALES * (1-SHARE_DOMESTIC_SALES)
    TOTAL_DOMESTIC_PRODUCTION_KG = TOTAL_ANNUAL_PRODUCTION_KG * SHARE_DOMESTIC_SALES
    
    if PRODUCT_TYPE == "Ammonia":
        
        #____VAT_DOMESTIC. E.g. thermal use of ammonia or other direct end-use.
        DOMESTIC_SALES_REVENUE_PRODUCT = TOTAL_DOMESTIC_PRODUCTION * (1-SHARE_NH3_FERTILIZER_DOMESTIC)
        DOMESTIC_SALES_REVENUE += DOMESTIC_SALES_REVENUE_PRODUCT
        EXPORT_SALES_REVENUE_PRODUCT = TOTAL_EXPORT_PRODUCTION
        EXPORT_SALES_REVENUE += EXPORT_SALES_REVENUE_PRODUCT

        if VAT_HYDROGEN_PRODUCT_BOOL:
            VAT_DOMESTIC = DOMESTIC_SALES_REVENUE_PRODUCT * VAT_RATE
        else:
            VAT_DOMESTIC = 0
        
        #____VAT_DRI
        VAT_DRI = 0
        
        #____VAT_FERTILIZER
        DOMESTIC_SALES_REVENUE_FERTILIZER = (
            TOTAL_DOMESTIC_PRODUCTION_KG * 
            SHARE_NH3_FERTILIZER_DOMESTIC * 
            FERTILIZER_PER_KG_NH3 * 
            FERTILIZER_SALES_PRICE * 
            SHARE_DOMESTIC_SALES_FERTILIZER)
        DOMESTIC_SALES_REVENUE += DOMESTIC_SALES_REVENUE_FERTILIZER
                
        EXPORT_SALES_REVENUE_FERTILIZER = (
            TOTAL_DOMESTIC_PRODUCTION_KG * 
            SHARE_NH3_FERTILIZER_DOMESTIC * 
            FERTILIZER_PER_KG_NH3 * 
            FERTILIZER_SALES_PRICE * 
            (1-SHARE_DOMESTIC_SALES_FERTILIZER))
        EXPORT_SALES_REVENUE += EXPORT_SALES_REVENUE_FERTILIZER

        if VAT_FERTILIZER_BOOL:
            VAT_FERTILIZER = (
                DOMESTIC_SALES_REVENUE_FERTILIZER * 
                VAT_RATE
                )
        else:
            VAT_FERTILIZER = 0

    
    elif PRODUCT_TYPE == "Hydrogen":
        #____VAT_DOMESTIC. E.g. thermal use of hydrogen. 
        DOMESTIC_SALES_REVENUE_PRODUCT = TOTAL_DOMESTIC_PRODUCTION * (1-SHARE_H2_DRI_DOMESTIC)
        DOMESTIC_SALES_REVENUE += DOMESTIC_SALES_REVENUE_PRODUCT
        EXPORT_SALES_REVENUE_PRODUCT = TOTAL_EXPORT_PRODUCTION
        EXPORT_SALES_REVENUE += EXPORT_SALES_REVENUE_PRODUCT

        if VAT_HYDROGEN_PRODUCT_BOOL:
            VAT_DOMESTIC = DOMESTIC_SALES_REVENUE_PRODUCT * VAT_RATE
        else:
            VAT_DOMESTIC = 0
        
        #____VAT_DRI
        DOMESTIC_SALES_REVENUE_DRI = ( 
            TOTAL_DOMESTIC_PRODUCTION_KG * 
            SHARE_H2_DRI_DOMESTIC * 
            DRI_PER_KG_H2 * 
            DRI_SALES_PRICE * 
            SHARE_DOMESTIC_SALES_DRI
            )
        DOMESTIC_SALES_REVENUE += DOMESTIC_SALES_REVENUE_DRI
        EXPORT_SALES_REVENUE_DRI = (
            TOTAL_DOMESTIC_PRODUCTION_KG * 
            SHARE_H2_DRI_DOMESTIC * 
            DRI_PER_KG_H2 * 
            DRI_SALES_PRICE * 
            (1-SHARE_DOMESTIC_SALES_DRI))
        EXPORT_SALES_REVENUE += EXPORT_SALES_REVENUE_DRI
        if VAT_DRI_BOOL:
            VAT_DRI = (
                DOMESTIC_SALES_REVENUE_DRI *
                VAT_RATE
                )
        else:
            VAT_DRI = 0
        #____VAT_FERTILIZER
        VAT_FERTILIZER = 0
        
    else:
        raise AttributeError("Unknown -PRODUCT_TYPE-")


    FISCAL_BENEFITS = (
        CORPORATE_TAX +
        VAT_INVEST + 
        IMPORT_DUTIES +
        VAT_HPA + 
        VAT_HSA +
        VAT_DOMESTIC +
        VAT_DRI +
        VAT_FERTILIZER
        )
    
    #Calculate fiscal expenses. (Cashflows to Hintco)
    FISCAL_EXPENSES = ANNUAL_FUNDING_LONG

    #Calculate NPV
    RELEVANT_CASHFLOWS = (
        FISCAL_BENEFITS -
        FISCAL_EXPENSES
        )
    
    #Discounting of annual cashflows and investments
    NPV = 0
    for t in range(DEPRECIATION_PERIOD):
        NPV += RELEVANT_CASHFLOWS[t] / (1+WACC)**t
        
    FISCAL_CASHFLOWS_DICT = {
        "FISCAL_EXPENSES" : -FISCAL_EXPENSES,
        "CORPORATE_TAX" : CORPORATE_TAX,
        "VAT_INVEST": VAT_INVEST, 
        "IMPORT_DUTIES": IMPORT_DUTIES,
        "VAT_HPA": VAT_HPA, 
        "VAT_HSA": VAT_HSA,
        "VAT_H2_PRODUCT": VAT_DOMESTIC,
        "VAT_DRI": VAT_DRI,
        "VAT_FERTILIZER": VAT_FERTILIZER
        }

    #calculate loan payments
    interest_payments = np.array([TOTAL_LOAN*WACC for t in range(DEPRECIATION_PERIOD)])
    
    if GRACE_PERIOD == 0:
        annual_principal = TOTAL_LOAN / DEPRECIATION_PERIOD
        principal_payments = np.array([annual_principal for t in range(DEPRECIATION_PERIOD)])
    else:
        annual_principal = TOTAL_LOAN / (DEPRECIATION_PERIOD-GRACE_PERIOD)
        principal_payments_I = np.array([0 for t in range(GRACE_PERIOD)])
        principal_payments_II = np.array([annual_principal for t in range(GRACE_PERIOD, DEPRECIATION_PERIOD)])
        principal_payments = np.concatenate((principal_payments_I, principal_payments_II), axis=0)

    LOAN_CASHFLOWS_DICT = {
        "INTEREST_PAYMENTS" : -interest_payments,
        "PRINCIPAL_PAYMENTS" : -principal_payments
        }

    SALES_REVENUES_DICT = {
        "DOMESTIC_SALES_REVENUE" : DOMESTIC_SALES_REVENUE,
        "EXPORT_SALES_REVENUE" : EXPORT_SALES_REVENUE
        }

    return NPV, FISCAL_CASHFLOWS_DICT, LOAN_CASHFLOWS_DICT, SALES_REVENUES_DICT