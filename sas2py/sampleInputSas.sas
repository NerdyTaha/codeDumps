data work.customer_summary;
    set raw.customers;
    where balance > 1000;
    risk_score = balance / 1000;
    if risk_score > 5 then risk_level = 'HIGH';
    else risk_level = 'LOW';
run;

proc means data=work.customer_summary mean std;
    var risk_score;
    class risk_level;
run;
