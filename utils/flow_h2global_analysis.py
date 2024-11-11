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
    
    Purchase_Price_Start = st.number_input(
        'Purchase price start [US$/kg]',
        value = 6.0,
        step=0.1,
        min_value=0.0,
        help="""The purchase price includes transport costs from the production site to the agreed demand location."""
        )
    Purchase_Price_End = st.number_input(
        'Purchase price end [US$/kg]',
        value = 6.0,
        step=0.1,
        min_value=0.0,
        help="""The purchase price includes transport costs from the production site to the agreed demand location."""
        )
    Sales_Price_Start = st.number_input(
        'Sales price start [US$/kg]',
        value = 3.0,
        step=0.1,
        min_value=0.0
        )

    Sales_Price_End = st.number_input(
        'Sales price end [US$/kg]',
        value = 4.5,
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
        WACC_PERCENT = st.number_input(
            'Cost of Capital [%]',
            value = 3.0,
            step=1.0,
            min_value=0.0,
            )
        WACC = WACC_PERCENT/100

        #Income tax
        #____Only consider corporate tax on revenue of production projects.
        CORPORATE_TAX_RATE_PERCENT = st.number_input(
            'Corporate tax rate [%]',
            value = 20,
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
        VAT_RATE_INVEST_PERCENT = st.number_input(
            'VAT rate on investments [%]',
            value = 10.0,
            step=1.0,
            min_value=0.0,
            )
        VAT_RATE_INVEST = VAT_RATE_INVEST_PERCENT / 100
        
        VAT_RATE_HPA_PERCENT = st.number_input(
            'VAT rate on HPA [%]',
            value = 10.0,
            step=1.0,
            min_value=0.0,
            )
        VAT_RATE_HPA = VAT_RATE_HPA_PERCENT / 100

        VAT_RATE_HSA_PERCENT = st.number_input(
            'VAT rate on HSA [%]',
            value = 10.0,
            step=1.0,
            min_value=0.0,
            )
        VAT_RATE_HSA = VAT_RATE_HSA_PERCENT / 100
        
        VAT_RATE_DRI_PERCENT = st.number_input(
            'VAT rate on DRI [%]',
            value = 10.0,
            step=1.0,
            min_value=0.0,
            )
        VAT_RATE_DRI = VAT_RATE_DRI_PERCENT / 100
        
        VAT_RATE_FERTILIZER_PERCENT = st.number_input(
            'VAT rate on fertilizer [%]',
            value = 10.0,
            step=1.0,
            min_value=0.0,
            )
        VAT_RATE_FERTILIZER = VAT_RATE_FERTILIZER_PERCENT / 100
        
        
        VAT_RATE_DOMESTIC_PERCENT = st.number_input(
            'VAT rate on domestic hydrogen product sales [%]',
            value = 10.0,
            step=1.0,
            min_value=0.0,
            )
        VAT_RATE_DOMESTIC = VAT_RATE_DOMESTIC_PERCENT / 100

        #Import duties
        IMPORT_DUTIES_RATE_PERCENT = st.number_input(
            'Import duties [%]',
            value = 10.0,
            step=1.0,
            min_value=0.0,
            )
        IMPORT_DUTIES_RATE = IMPORT_DUTIES_RATE_PERCENT / 100

        #SHARES
        SHARE_HPA_CONTRACT_PERCENT = st.number_input(
            'Share of the HPA contract of total production [%]',
            value = 50,
            step=1,
            min_value=0,
            )
        SHARE_HPA_CONTRACT = SHARE_HPA_CONTRACT_PERCENT/100
        
        SHARE_TAXABLE_INCOME_PERCENT = st.number_input(
            'Share of taxable income of total revenue of the production project [%]',
            value = 50,
            step=1,
            min_value=0,
            )
        SHARE_TAXABLE_INCOME = SHARE_TAXABLE_INCOME_PERCENT/100
        
        SHARE_DOMESTIC_SALES_PERCENT = st.number_input(
            'Share of total product hydrogen product which is sold domestically [%]',
            value = 80,
            step = 1,
            min_value=0,
            )
        SHARE_DOMESTIC_SALES = SHARE_DOMESTIC_SALES_PERCENT/100

        SHARE_IMPORTED_PRODUCTION_EQUIPMENT_PERCENT = st.number_input(
            'Share of the production equipment which is imported [%]',
            value = 80,
            step = 1,
            min_value=0,
            help="E.g. electrolyser imported from other country."
            )
        SHARE_IMPORTED_PRODUCTION_EQUIPMENT = SHARE_IMPORTED_PRODUCTION_EQUIPMENT_PERCENT/100

        SHARE_H2_DRI_DOMESTIC_PERCENT = st.number_input(
            'Share of hydrogen which is used for the domestic production of DRI [%]',
            value = 80,
            step = 1,
            min_value=0,
            help="only relevant for hydrogen production"
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
            help="only relevant for hydrogen production"
            )
        SHARE_DOMESTIC_SALES_DRI = SHARE_DOMESTIC_SALES_DRI_PERCENT/100

        SHARE_NH3_FERTILIZER_DOMESTIC_PERCENT = st.number_input(
            'Share of ammonia which is used for the domestic production of fertilizer [%]',
            value = 80,
            step = 1,
            min_value=0,
            help="only relevant for ammonia production"
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

        SHARE_DOMESTIC_SALES_FERTILIZER = st.number_input(
            'Share of fertilizer which is sold domestically [%]',
            value = 100,
            step = 1,
            min_value=0,
            help="only relevant for ammonia production"
            )
        SHARE_DOMESTIC_SALES_DRI = SHARE_DOMESTIC_SALES_DRI_PERCENT/100
        
    
    st.markdown("**Which metrics do you want to visualize?**")
    
    VIS_0=st.checkbox(label="Traded energy [US$]")
    VIS_1=st.checkbox(label="Traded energy [tons]")
    VIS_2_A=st.checkbox(label="Annual funding spent [US$]")
    VIS_2_B=st.checkbox(label="Total funding spent [US$]")
    VIS_3=st.checkbox(label="Mitigated CO2-emissions [tons]")
    VIS_4=st.checkbox(label="Required electrolyzer capacity [GW]")
    VIS_5=st.checkbox(label="Visualize net-present value of fiscal benefits to the state [US$]")
    VIS_6=st.checkbox(label="Visualize fiscal cashflows [US$]")
    
    
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
            
            FISCAL_NPV, FISCAL_CASHFLOWS_DICT = get_fiscal_npv(
                    PRODUCT_TYPE=Derivative,
                    ANNUAL_PRODUCTION=data_to_plot["Hydrogen Purchases [kg]"], #kg
                    ANNUAL_PRODUCT_PURCHASES=data_to_plot["Hydrogen Purchases [$]"], #USD
                    ANNUAL_PRODUCT_SALES=data_to_plot["Annual Sales [$]"], #USD
                    ANNUAL_FUNDING=data_to_plot["Used Funding Volume [$]"], #USD   
                    DEPRECIATION_PERIOD=DEPRECIATION_PERIOD, #YEARS
                    CONTRACT_PERIOD_HPA=Period,
                    WACC=WACC,
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
                    VAT_RATE_INVEST=VAT_RATE_INVEST,
                    IMPORT_DUTIES_RATE=IMPORT_DUTIES_RATE,
                    VAT_RATE_HPA=VAT_RATE_HPA,
                    VAT_RATE_HSA=VAT_RATE_HSA,
                    VAT_RATE_DOMESTIC=VAT_RATE_DOMESTIC,
                    VAT_RATE_DRI=VAT_RATE_DRI,
                    VAT_RATE_FERTILIZER=VAT_RATE_FERTILIZER
                    )
            
            if VIS_5:
                # Convert dictionary to lists for Plotly
                categories = list(FISCAL_CASHFLOWS_DICT.keys())
                
                FISCAL_CASHFLOWS_DICT_DEPRECIATED = {}
                for c in categories:
                    CASHFLOW_DEPRECIATED_TEMP = 0
                    FISCAL_CASHFLOWS_TEMP = FISCAL_CASHFLOWS_DICT[c]
                    if isinstance(FISCAL_CASHFLOWS_TEMP, (int, float)):
                        FISCAL_CASHFLOWS_DICT_DEPRECIATED[c] = FISCAL_CASHFLOWS_TEMP
                        continue
                    else:
                        for t in range(DEPRECIATION_PERIOD):
                            CASHFLOW_DEPRECIATED_TEMP += FISCAL_CASHFLOWS_TEMP[t] / (1+WACC)**t
    
                    FISCAL_CASHFLOWS_DICT_DEPRECIATED[c] = CASHFLOW_DEPRECIATED_TEMP
                
                #Extract keys and values from dict for visualization
                categories_vis = list(FISCAL_CASHFLOWS_DICT_DEPRECIATED.keys())
                values_vis = list(FISCAL_CASHFLOWS_DICT_DEPRECIATED.values())
                
                # Create a Plotly Express bar chart
                fig5 = px.bar(
                    x=categories_vis,
                    y=values_vis,
                    labels={'y': 'Cashflow [US$]'},
                    title="Depreciated Cashflow [US$]",
                    text=values_vis  # Display float values on bars
                )
                
                # Customize the bar chart
                fig5.update_traces(texttemplate='%{text:.2f}', textposition='outside')  # Format text to 2 decimals
                fig5.update_layout(yaxis=dict(title="Values"), xaxis=dict(title="Categories"))
                
                # Display the chart in Streamlit
                st.plotly_chart(fig5)         
                
                st.write(
                    "Net-present value of funding instrument for fiscal authority:", 
                    round(FISCAL_NPV*1e-6, 2), 
                    "[Million US$]"
                    )
    
            if VIS_6:
                
                fig6 = go.Figure()
                
                #Plot hydrogen purchases
                data_to_plot_long = pd.DataFrame(
                    {
                       "Year": range(1,DEPRECIATION_PERIOD+1)
                       }
                    )
                                
                categories = list(FISCAL_CASHFLOWS_DICT.keys())
                for c in categories:
                    #Adding data
                    data_to_plot_long[c] = FISCAL_CASHFLOWS_DICT[c]                    
                
                    #Add bar for Hydrogen Purchases from Funding with error bars
                    fig6.add_trace(go.Bar(
                        x=data_to_plot_long['Year'],
                        y=data_to_plot_long[c],
                        name=c
                        )
                    )
        
                # Update layout to stack bars
                fig6.update_layout(
                    title="Absolute fiscal cashflows [US$]",
                    barmode='stack',  # Stack bars
                    xaxis_title='Year',
                    yaxis_title="Cashflow [US$]",
                )
                
                # Render the Plotly chart in Streamlit
                st.plotly_chart(fig6, use_container_width=True)
               
            
def get_fiscal_npv(
        PRODUCT_TYPE,
        ANNUAL_PRODUCTION, #kg
        ANNUAL_PRODUCT_PURCHASES, #USD
        ANNUAL_PRODUCT_SALES, #USD
        ANNUAL_FUNDING, #USD
        DEPRECIATION_PERIOD, #YEARS
        CONTRACT_PERIOD_HPA, #years
        WACC,
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
        VAT_RATE_INVEST,
        IMPORT_DUTIES_RATE,
        VAT_RATE_HPA,
        VAT_RATE_HSA,
        VAT_RATE_DOMESTIC,
        VAT_RATE_DRI,
        VAT_RATE_FERTILIZER
        ):
    
    if CONTRACT_PERIOD_HPA > DEPRECIATION_PERIOD:
        raise ValueError("Depreciation period of loan is shorter than HPA contract period.")
    else:
        delta_years = DEPRECIATION_PERIOD - CONTRACT_PERIOD_HPA
        
        #resize external input arrays.
        ANNUAL_PRODUCTION = np.concatenate([ANNUAL_PRODUCTION, np.full(delta_years, ANNUAL_PRODUCTION.iloc[-1])]) #kg
        ANNUAL_PRODUCT_PURCHASES = np.concatenate([ANNUAL_PRODUCT_PURCHASES, np.full(delta_years, ANNUAL_PRODUCT_PURCHASES.iloc[-1])]) #USD
        ANNUAL_PRODUCT_SALES = np.concatenate([ANNUAL_PRODUCT_SALES, np.zeros(delta_years)]) #USD
        ANNUAL_FUNDING_LONG = np.concatenate([ANNUAL_FUNDING, np.zeros(delta_years)]) #USD
        
    #Calculate fiscal benefits. (tax revenues)
    #____CORPORATE_TAX: Only include supply side, because these will be genuinely new businesses.
    TOTAL_ANNUAL_PRODUCTION = ANNUAL_PRODUCT_PURCHASES / SHARE_HPA_CONTRACT
    TOTAL_ANNUAL_PRODUCTION_KG = ANNUAL_PRODUCTION / SHARE_HPA_CONTRACT
    TAXABLE_INCOME = TOTAL_ANNUAL_PRODUCTION * SHARE_TAXABLE_INCOME
    CORPORATE_TAX = TAXABLE_INCOME * CORPORATE_TAX_RATE
    
    #____VAT_RATE_INVEST: Includes the VAT on initial investments on the supply side.
    VAT_INVEST = np.zeros(DEPRECIATION_PERIOD)
    if PRODUCT_TYPE == "Ammonia":
        CAPEX_PER_KG_ANNUAL_PRODUCTION = 10 #Evaluation Kenya White Paper: 5.2 (Turkana South 500 MW), Turkana Central 10 MW: 10.6, Kisumu 10GW: 15.7 €/kg NH3/year
    elif PRODUCT_TYPE == "Hydrogen":
        CAPEX_PER_KG_ANNUAL_PRODUCTION = 45 #Evaluation Kenya White Paper: 22.3 (Turkana South 500 MW), Turkana Central 10 MW: 38.4, Kisumu 10GW: 57.5 €/kg H2/year 
    else:
        raise AttributeError("Unknown -PRODUCT_TYPE-")
        
    CAPEX = np.max(ANNUAL_PRODUCTION) * CAPEX_PER_KG_ANNUAL_PRODUCTION
    VAT_INVEST[0] = CAPEX * VAT_RATE_INVEST
    
    #____IMPORT_DUTIES_RATE
    IMPORT_DUTIES = np.zeros(DEPRECIATION_PERIOD)
    IMPORT_DUTIES[0] = CAPEX * SHARE_IMPORTED_PRODUCTION_EQUIPMENT * IMPORT_DUTIES_RATE
    
    #____VAT_HPA
    VAT_HPA = 0 #Assume this to be zero. VAT_RATE_HPA * ANNUAL_PRODUCT_PURCHASES
    
    #____VAT_HSA
    VAT_HSA = 0 #Assume this to be zero. VAT_RATE_HSA * ANNUAL_PRODUCT_SALES
        
    TOTAL_DOMESTIC_PRODUCTION = TOTAL_ANNUAL_PRODUCTION * SHARE_DOMESTIC_SALES
    TOTAL_DOMESTIC_PRODUCTION_KG = TOTAL_ANNUAL_PRODUCTION_KG * SHARE_DOMESTIC_SALES
    
    if PRODUCT_TYPE == "Ammonia":
        #____VAT_DOMESTIC. E.g. thermal use of ammonia or other direct end-use.
        VAT_DOMESTIC = TOTAL_DOMESTIC_PRODUCTION * (1-SHARE_NH3_FERTILIZER_DOMESTIC) * VAT_RATE_DOMESTIC
        #____VAT_DRI
        VAT_DRI = 0
        #____VAT_FERTILIZER
        VAT_FERTILIZER = ( 
            TOTAL_DOMESTIC_PRODUCTION_KG * 
            SHARE_NH3_FERTILIZER_DOMESTIC * 
            FERTILIZER_PER_KG_NH3 * 
            FERTILIZER_SALES_PRICE * 
            SHARE_DOMESTIC_SALES_FERTILIZER * 
            VAT_RATE_FERTILIZER
            )

    
    elif PRODUCT_TYPE == "Hydrogen":
        #____VAT_DOMESTIC. E.g. thermal use of hydrogen. 
        VAT_DOMESTIC = TOTAL_DOMESTIC_PRODUCTION * (1-SHARE_H2_DRI_DOMESTIC) * VAT_RATE_DOMESTIC
        #____VAT_DRI
        VAT_DRI = ( 
            TOTAL_DOMESTIC_PRODUCTION_KG * 
            SHARE_H2_DRI_DOMESTIC * 
            DRI_PER_KG_H2 * 
            DRI_SALES_PRICE * 
            SHARE_DOMESTIC_SALES_DRI * 
            VAT_RATE_DRI
            )
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
        "VAT_DOMESTIC": VAT_DOMESTIC,
        "VAT_DRI": VAT_DRI,
        "VAT_FERTILIZER": VAT_FERTILIZER
        }

    return NPV, FISCAL_CASHFLOWS_DICT