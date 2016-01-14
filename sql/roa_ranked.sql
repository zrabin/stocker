SELECT company.symbol, company.name, financialdata.return_on_assets 
FROM company inner join financialdata 
ON company.id = financialdata.company_id 
--ORDER BY financialdata.return_on_assets
ORDER BY company.symbol
DESC;
