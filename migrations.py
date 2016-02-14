from playhouse.migrate import *

my_db = SqliteDatabase('stocker.db')
migrator = SqliteMigrator(my_db)

rank_ask = DecimalField(null=True)
rank_book_value = DecimalField(null=True)
rank_market_cap = DecimalField(null=True)
rank_ebitda = DecimalField(null=True)
rank_pe_ratio_ttm = DecimalField(null=True)
rank_pe_ratio_ftm = DecimalField(null=True)
rank_eps_estimate_qtr = DecimalField(null=True)
rank_peg_ratio = DecimalField(null=True)
rank_return_on_assets = DecimalField(null=True)
rank_return_on_equity = DecimalField(null=True)
rank_change_year_low_per = DecimalField(null=True)
rank_change_year_high_per = DecimalField(null=True)
rank_one_yr_target_price = DecimalField(null=True)
rank_net_income = DecimalField(null=True)
rank_total_assets = DecimalField(null=True)
rank_OneyrTargetPrice = DecimalField(null=True)
rank_DividendYield = DecimalField(null=True)
rank_EPSEstimateCurrentYear = DecimalField(null=True)
rank_EPSEstimateNextYear = DecimalField(null=True)
rank_EPSEstimateNextQuarter = DecimalField(null=True)

migrate(
migrator.drop_column('financialdata', 'rank_ask'),
migrator.drop_column('financialdata', 'rank_book_value'),
migrator.drop_column('financialdata', 'rank_market_cap'),
migrator.drop_column('financialdata', 'rank_ebitda'),
migrator.drop_column('financialdata', 'rank_pe_ratio_ttm'),
migrator.drop_column('financialdata', 'rank_pe_ratio_ftm'),
migrator.drop_column('financialdata', 'rank_eps_estimate_qtr'),
migrator.drop_column('financialdata', 'rank_peg_ratio'),
migrator.drop_column('financialdata', 'rank_one_yr_target_price'),
migrator.drop_column('financialdata', 'rank_return_on_assets'),
migrator.drop_column('financialdata', 'rank_return_on_equity'),
migrator.drop_column('financialdata', 'rank_change_year_low_per'),
migrator.drop_column('financialdata', 'rank_change_year_high_per'),
migrator.drop_column('financialdata', 'rank_net_income'),
migrator.drop_column('financialdata', 'rank_total_assets'),
migrator.drop_column('financialdata', 'rank_OneyrTargetPrice'),
migrator.drop_column('financialdata', 'rank_DividendYield'),
migrator.drop_column('financialdata', 'rank_EPSEstimateCurrentYear'),
migrator.drop_column('financialdata', 'rank_EPSEstimateNextYear'),
migrator.drop_column('financialdata', 'rank_EPSEstimateNextQuarter'),
migrator.add_column('financialdata', 'rank_ask', rank_ask),
migrator.add_column('financialdata', 'rank_book_value', rank_book_value),
migrator.add_column('financialdata', 'rank_market_cap', rank_market_cap),
migrator.add_column('financialdata', 'rank_ebitda', rank_ebitda),
migrator.add_column('financialdata', 'rank_pe_ratio_ttm', rank_pe_ratio_ttm),
migrator.add_column('financialdata', 'rank_pe_ratio_ftm', rank_pe_ratio_ftm),
migrator.add_column('financialdata', 'rank_eps_estimate_qtr', rank_eps_estimate_qtr),
migrator.add_column('financialdata', 'rank_peg_ratio', rank_peg_ratio),
migrator.add_column('financialdata', 'rank_one_yr_target_price', rank_one_yr_target_price),
migrator.add_column('financialdata', 'rank_return_on_assets', rank_return_on_assets),
migrator.add_column('financialdata', 'rank_return_on_equity', rank_return_on_equity),
migrator.add_column('financialdata', 'rank_change_year_low_per', rank_change_year_low_per),
migrator.add_column('financialdata', 'rank_change_year_high_per', rank_change_year_high_per),
migrator.add_column('financialdata', 'rank_net_income', rank_net_income),
migrator.add_column('financialdata', 'rank_total_assets', rank_total_assets),
migrator.add_column('financialdata', 'rank_OneyrTargetPrice', rank_OneyrTargetPrice),
migrator.add_column('financialdata', 'rank_DividendYield', rank_DividendYield),
migrator.add_column('financialdata', 'rank_EPSEstimateCurrentYear', rank_EPSEstimateCurrentYear),
migrator.add_column('financialdata', 'rank_EPSEstimateNextYear', rank_EPSEstimateNextYear),
migrator.add_column('financialdata', 'rank_EPSEstimateNextQuarter', rank_EPSEstimateNextQuarter)
)



#pe_ratio_ftm = DecimalField(null=True)
#rank_pe_ratio_ftm = DecimalField(null=True)

#migrate(
#    migrator.add_column('financialdata', 'pe_ratio_ftm', pe_ratio_ftm),
#    migrator.add_column('financialdata', 'rank_pe_ratio_ftm', rank_pe_ratio_ftm),
#    migrator.drop_column('some_table', 'old_column'),
#)
