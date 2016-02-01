select company.symbol, financialdata.pe_ratio_ttm, financialdata.return_on_assets from company inner join financialdata on company.id = financialdata.company_id where financialdata.return_on_assets is not null and financialdata.pe_ratio_ttm is not null order by company.symbol limit 3;



select company.symbol, financialdata.pe_ratio_ttm, financialdata.return_on_assets from company inner join financialdata on company.id = financialdata.company_id where financialdata.pe_ratio_ttm IS NOT Null order by company.symbol limit 10;

select company.symbol, financialdata.pe_ratio_ttm, financialdata.return_on_assets from company inner join financialdata on company.id = financialdata.company_id where financialdata.return_on_assets IS NOT Null order by company.symbol limit 10;
