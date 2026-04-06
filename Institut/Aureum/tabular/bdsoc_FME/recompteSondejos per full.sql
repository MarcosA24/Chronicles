select ts.id 'fullID',ts.id25mabs, count(ts.fid)'nombre sondejos' from(
	select s.*,t.id,t.id25mabs from tall25m t
	join sondeig s on st_within(s.geom,t.geom)
	)ts
group by ts.id,ts.id25mabs