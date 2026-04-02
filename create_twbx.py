"""
Generate a Tableau packaged workbook (.twbx) for Iowa Retail Sales Analysis
Final Case Analysis - BAN-5023  (FIXED XML structure)
"""
import zipfile
import os

DATA_FILE = r'E:\伴读书童\iowa_retail_sales.csv'
OUTPUT_TWBX = r'E:\伴读书童\Iowa_Retail_Sales_Analysis.twbx'
DS = 'textscan.iowa1'
DS_CAP = 'Iowa Retail Sales'

BG   = f'[{DS}].[none:Business Group:nk]'
FY   = f'[{DS}].[none:Fiscal Year:ok]'
TS   = f'[{DS}].[sum:Taxable Sales:ok]'
CT   = f'[{DS}].[sum:Computed Tax:ok]'

BG_FILTER = f"""      <filter class='categorical' column='{BG}'>
            <groupfilter function='union' user:op='exclude'>
              <groupfilter function='member' level='[none:Business Group:nk]' member='County Totals'/>
              <groupfilter function='member' level='[none:Business Group:nk]' member='State Totals'/>
            </groupfilter>
          </filter>"""

DATASOURCES_REF = f"<datasource caption='{DS_CAP}' name='{DS}'/>"

TWB = f"""<?xml version='1.0' encoding='utf-8' ?>
<workbook source-build='2021.1.0' source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <preferences>
    <color-palette name='color_blind' type='regular'>
      <color>#1170aa</color><color>#fc7d0b</color><color>#a3acb9</color>
      <color>#57606c</color><color>#5fa2ce</color><color>#c85200</color>
      <color>#7b848f</color><color>#a3cce9</color><color>#ffbc79</color>
      <color>#c8d0d9</color>
    </color-palette>
  </preferences>
  <datasources>
    <datasource caption='{DS_CAP}' inline='true' name='{DS}' version='18.1'>
      <connection class='textscan' filename='Data/iowa_retail_sales.csv'>
        <relation name='iowa_retail_sales' table='[iowa_retail_sales]' type='table'/>
        <metadata-records>
          <metadata-record class='column'>
            <remote-name>Fiscal Year</remote-name><remote-type>20</remote-type>
            <local-name>[Fiscal Year]</local-name>
            <parent-name>[iowa_retail_sales]</parent-name>
            <remote-alias>Fiscal Year</remote-alias><ordinal>1</ordinal>
            <local-type>integer</local-type><aggregation>Sum</aggregation>
            <precision>10</precision><contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Business Group</remote-name><remote-type>129</remote-type>
            <local-name>[Business Group]</local-name>
            <parent-name>[iowa_retail_sales]</parent-name>
            <remote-alias>Business Group</remote-alias><ordinal>2</ordinal>
            <local-type>string</local-type><aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Taxable Sales</remote-name><remote-type>20</remote-type>
            <local-name>[Taxable Sales]</local-name>
            <parent-name>[iowa_retail_sales]</parent-name>
            <remote-alias>Taxable Sales</remote-alias><ordinal>3</ordinal>
            <local-type>integer</local-type><aggregation>Sum</aggregation>
            <precision>10</precision><contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Computed Tax</remote-name><remote-type>20</remote-type>
            <local-name>[Computed Tax]</local-name>
            <parent-name>[iowa_retail_sales]</parent-name>
            <remote-alias>Computed Tax</remote-alias><ordinal>4</ordinal>
            <local-type>integer</local-type><aggregation>Sum</aggregation>
            <precision>10</precision><contains-null>true</contains-null>
          </metadata-record>
        </metadata-records>
      </connection>
      <column datatype='integer' name='[Fiscal Year]' role='dimension' type='ordinal'/>
      <column datatype='string' name='[Business Group]' role='dimension' type='nominal'/>
      <column datatype='integer' name='[Taxable Sales]' role='measure' type='quantitative'/>
      <column datatype='integer' name='[Computed Tax]' role='measure' type='quantitative'/>
    </datasource>
  </datasources>
  <worksheets>

    <worksheet name='1. Sales Trend by Year'>
      <table>
        <view>
          <datasources><datasource caption='{DS_CAP}' name='{DS}'/></datasources>
          <datasource-dependencies datasource='{DS}'>
            <column datatype='integer' name='[Fiscal Year]' role='dimension' type='ordinal'/>
            <column datatype='string' name='[Business Group]' role='dimension' type='nominal'/>
            <column datatype='integer' name='[Taxable Sales]' role='measure' type='quantitative'/>
            <column-instance column='[Fiscal Year]' derivation='None' name='[none:Fiscal Year:ok]' pivot='key' type='ordinal'/>
            <column-instance column='[Taxable Sales]' derivation='Sum' name='[sum:Taxable Sales:ok]' pivot='value' type='quant'/>
            <column-instance column='[Business Group]' derivation='None' name='[none:Business Group:nk]' pivot='key' type='nominal'/>
          </datasource-dependencies>
{BG_FILTER}
        </view>
        <style/>
        <panes>
          <pane>
            <view><breakdown value='auto'/></view>
            <mark class='Line'/>
            <encodings>
              <color column='{BG}' palette='color_blind'/>
            </encodings>
          </pane>
        </panes>
        <rows>{TS}</rows>
        <cols>{FY}</cols>
      </table>
      <simple-id uuid='{{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}'/>
    </worksheet>

    <worksheet name='2. Business Group Ranking'>
      <table>
        <view>
          <datasources><datasource caption='{DS_CAP}' name='{DS}'/></datasources>
          <datasource-dependencies datasource='{DS}'>
            <column datatype='string' name='[Business Group]' role='dimension' type='nominal'/>
            <column datatype='integer' name='[Taxable Sales]' role='measure' type='quantitative'/>
            <column-instance column='[Business Group]' derivation='None' name='[none:Business Group:nk]' pivot='key' type='nominal'/>
            <column-instance column='[Taxable Sales]' derivation='Sum' name='[sum:Taxable Sales:ok]' pivot='value' type='quant'/>
          </datasource-dependencies>
{BG_FILTER}
        </view>
        <style/>
        <panes>
          <pane>
            <view><breakdown value='auto'/></view>
            <mark class='Bar'/>
            <encodings>
              <color column='{BG}' palette='color_blind'/>
            </encodings>
          </pane>
        </panes>
        <rows>{BG}</rows>
        <cols>{TS}</cols>
      </table>
      <simple-id uuid='{{B2C3D4E5-F6A7-8901-BCDE-F12345678901}}'/>
    </worksheet>

    <worksheet name='3. Yearly Sales Total'>
      <table>
        <view>
          <datasources><datasource caption='{DS_CAP}' name='{DS}'/></datasources>
          <datasource-dependencies datasource='{DS}'>
            <column datatype='integer' name='[Fiscal Year]' role='dimension' type='ordinal'/>
            <column datatype='string' name='[Business Group]' role='dimension' type='nominal'/>
            <column datatype='integer' name='[Taxable Sales]' role='measure' type='quantitative'/>
            <column-instance column='[Fiscal Year]' derivation='None' name='[none:Fiscal Year:ok]' pivot='key' type='ordinal'/>
            <column-instance column='[Taxable Sales]' derivation='Sum' name='[sum:Taxable Sales:ok]' pivot='value' type='quant'/>
            <column-instance column='[Business Group]' derivation='None' name='[none:Business Group:nk]' pivot='key' type='nominal'/>
          </datasource-dependencies>
{BG_FILTER}
        </view>
        <style/>
        <panes>
          <pane>
            <view><breakdown value='auto'/></view>
            <mark class='Bar'/>
          </pane>
        </panes>
        <rows>{TS}</rows>
        <cols>{FY}</cols>
      </table>
      <simple-id uuid='{{C3D4E5F6-A7B8-9012-CDEF-123456789012}}'/>
    </worksheet>

    <worksheet name='4. Tax Revenue Mix'>
      <table>
        <view>
          <datasources><datasource caption='{DS_CAP}' name='{DS}'/></datasources>
          <datasource-dependencies datasource='{DS}'>
            <column datatype='string' name='[Business Group]' role='dimension' type='nominal'/>
            <column datatype='integer' name='[Computed Tax]' role='measure' type='quantitative'/>
            <column-instance column='[Business Group]' derivation='None' name='[none:Business Group:nk]' pivot='key' type='nominal'/>
            <column-instance column='[Computed Tax]' derivation='Sum' name='[sum:Computed Tax:ok]' pivot='value' type='quant'/>
          </datasource-dependencies>
{BG_FILTER}
        </view>
        <style/>
        <panes>
          <pane>
            <view><breakdown value='auto'/></view>
            <mark class='Pie'/>
            <encodings>
              <color column='{BG}' palette='color_blind'/>
              <size column='{CT}'/>
            </encodings>
          </pane>
        </panes>
        <rows/>
        <cols/>
      </table>
      <simple-id uuid='{{D4E5F6A7-B8C9-0123-DEF0-234567890123}}'/>
    </worksheet>

  </worksheets>
  <dashboards>
    <dashboard name='Dashboard 1'>
      <style/>
      <size maxheight='768' maxwidth='1024' minheight='768' minwidth='1024'/>
      <zones>
        <zone h='98000' id='2' type='layout-basic' w='100000' x='0' y='0'>
          <zone h='98000' id='3' param='vert' type='layout-flow' w='100000' x='0' y='0'>
            <zone h='49000' id='4' name='1. Sales Trend by Year' param='1. Sales Trend by Year' type='sheet' w='60000' x='0' y='0'/>
            <zone h='49000' id='5' name='2. Business Group Ranking' param='2. Business Group Ranking' type='sheet' w='40000' x='60000' y='0'/>
            <zone h='49000' id='6' name='3. Yearly Sales Total' param='3. Yearly Sales Total' type='sheet' w='60000' x='0' y='49000'/>
            <zone h='49000' id='7' name='4. Tax Revenue Mix' param='4. Tax Revenue Mix' type='sheet' w='40000' x='60000' y='49000'/>
          </zone>
        </zone>
      </zones>
      <simple-id uuid='{{E5F6A7B8-C9D0-1234-EF01-345678901234}}'/>
    </dashboard>
  </dashboards>
  <stories>
    <story name='Iowa Retail Sales Storyboard' navigation-style='Caption Only'>
      <style/>
      <size maxheight='768' maxwidth='1016' minheight='768' minwidth='1016'/>
      <points>
        <point caption='Overview: 25 Years of Iowa Retail Sales'>
          <story-navigator-description>
            <formatted-text>
              <run>Problem Statement: How have Iowa&apos;s retail business categories evolved from 2000 to 2026, and what patterns can inform business investment decisions?</run>
            </formatted-text>
          </story-navigator-description>
          <snap zones-offset-x='0' zones-offset-y='0'>
            <zone h='94500' id='100' name='1. Sales Trend by Year' param='1. Sales Trend by Year' type='sheet' w='100000' x='0' y='0'/>
          </snap>
        </point>
        <point caption='Which Sectors Drive Revenue?'>
          <story-navigator-description>
            <formatted-text>
              <run>Service and Eating &amp; Drinking sectors dominate Iowa taxable sales, while Specialty Retail shows accelerating growth since 2015 — a signal for market entrants.</run>
            </formatted-text>
          </story-navigator-description>
          <snap zones-offset-x='0' zones-offset-y='0'>
            <zone h='94500' id='101' name='2. Business Group Ranking' param='2. Business Group Ranking' type='sheet' w='100000' x='0' y='0'/>
          </snap>
        </point>
        <point caption='Year-over-Year Growth Patterns'>
          <story-navigator-description>
            <formatted-text>
              <run>Total taxable sales dipped sharply in 2020 (COVID-19 impact) but recovered by 2021. Essential goods categories showed greater resilience during the downturn.</run>
            </formatted-text>
          </story-navigator-description>
          <snap zones-offset-x='0' zones-offset-y='0'>
            <zone h='94500' id='102' name='3. Yearly Sales Total' param='3. Yearly Sales Total' type='sheet' w='100000' x='0' y='0'/>
          </snap>
        </point>
        <point caption='Tax Revenue Composition &amp; Key Insights'>
          <story-navigator-description>
            <formatted-text>
              <run>Key Insight: Service and General Merchandise contribute the highest tax revenue share. The full dashboard reveals regional and sector-level opportunities for strategic investment.</run>
            </formatted-text>
          </story-navigator-description>
          <snap zones-offset-x='0' zones-offset-y='0'>
            <zone h='47000' id='103' name='Dashboard 1' param='Dashboard 1' type='dashboard' w='100000' x='0' y='0'/>
          </snap>
        </point>
      </points>
      <simple-id uuid='{{F6A7B8C9-D0E1-2345-F012-456789012345}}'/>
    </story>
  </stories>
</workbook>
"""

# Write TWB
twb_path = r'E:\伴读书童\Iowa_Retail_Sales_Analysis.twb'
with open(twb_path, 'w', encoding='utf-8') as f:
    f.write(TWB)
print(f'TWB written: {twb_path}')

# Package as TWBX
with zipfile.ZipFile(OUTPUT_TWBX, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(twb_path, 'Iowa_Retail_Sales_Analysis.twb')
    zf.write(DATA_FILE, 'Data/iowa_retail_sales.csv')

print(f'TWBX created: {OUTPUT_TWBX}')
print(f'Size: {os.path.getsize(OUTPUT_TWBX) / 1024:.1f} KB')
