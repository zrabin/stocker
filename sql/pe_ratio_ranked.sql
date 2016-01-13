SELECT company.symbol, company.name, financialdata.pe_ratio_ttm 
FROM company inner join financialdata 
ON company.id = financialdata.company_id 
WHERE financialdata.pe_ratio_ttm > 0 
ORDER BY financialdata.pe_ratio_ttm 
DESC;
