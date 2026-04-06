update tall25m
set num_sondej= sel.recompte
from
	tall25m t
	Left JOIN
	(select count(ts.fid)'recompte',ts.id 'fullID',ts.id25mabs'idmabs' from(
		select s.*,t.id,t.id25mabs from tall25m t
		join sondeig s on st_within(s.geom,t.geom)
		)ts
	group by ts.id,ts.id25mabs)sel 
	on sel.idmabs=t.id25mabs;