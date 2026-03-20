import { useState } from "react";

export default function TopCustomers({ data }) {

const [search,setSearch] = useState("");

const filteredCustomers = data.filter((c)=>
c.name.toLowerCase().includes(search.toLowerCase())
)

return (

<div className="card">

<h3>Top Customers</h3>

<input
placeholder="Search customer..."
value={search}
onChange={(e)=>setSearch(e.target.value)}
style={{marginBottom:"10px",padding:"5px"}}
/>

<table>

<thead>
<tr>
<th>Name</th>
<th>Region</th>
<th>Total Spend</th>
<th>Churn</th>
</tr>
</thead>

<tbody>

{filteredCustomers.map((c,i)=>(
<tr key={i}>
<td>{c.name}</td>
<td>{c.region}</td>
<td>{c.total_spend}</td>
<td>{String(c.churned)}</td>
</tr>
))}

</tbody>

</table>

</div>

)

}