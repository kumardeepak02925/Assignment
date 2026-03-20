import { useEffect, useState } from "react";
import {
LineChart,
Line,
XAxis,
YAxis,
Tooltip,
ResponsiveContainer,
BarChart,
Bar
} from "recharts";

import "./App.css";

const API="http://127.0.0.1:8000/api";

function App(){

const[revenue,setRevenue]=useState([]);
const[categories,setCategories]=useState([]);
const[customers,setCustomers]=useState([]);
const[regions,setRegions]=useState([]);

const[loading,setLoading]=useState(true);
const[error,setError]=useState(null);


useEffect(()=>{

async function load(){

try{

const r1=await fetch(`${API}/revenue`);
const r2=await fetch(`${API}/categories`);
const r3=await fetch(`${API}/top-customers`);
const r4=await fetch(`${API}/regions`);

setRevenue((await r1.json()).data);
setCategories((await r2.json()).data);
setCustomers((await r3.json()).data);
setRegions((await r4.json()).data);

setLoading(false);

}catch(e){

setError("Failed to load API data");
setLoading(false);

}

}

load();

},[]);


if(loading) return <h2>Loading dashboard...</h2>;
if(error) return <h2>{error}</h2>;


/* KPI calculations */

const totalRevenue = regions.reduce((sum,r)=>sum+r.total_revenue,0);
const totalOrders = regions.reduce((sum,r)=>sum+r.orders,0);
const totalCustomers = regions.reduce((sum,r)=>sum+r.customers,0);
const totalCategories = categories.length;


return(

<div className="container">

<h1>Business Analytics Dashboard</h1>


{/* KPI CARDS */}

<div className="kpi-grid">

<div className="kpi-card">
<h3>Total Revenue</h3>
<p>${totalRevenue}</p>
</div>

<div className="kpi-card">
<h3>Total Orders</h3>
<p>{totalOrders}</p>
</div>

<div className="kpi-card">
<h3>Customers</h3>
<p>{totalCustomers}</p>
</div>

<div className="kpi-card">
<h3>Categories</h3>
<p>{totalCategories}</p>
</div>

</div>


{/* CHARTS */}

<div className="chart-grid">

<div className="card">

<h3>Revenue Trend</h3>

<ResponsiveContainer width="100%" height={300}>
<LineChart data={revenue}>
<XAxis dataKey="order_year_month"/>
<YAxis/>
<Tooltip/>
<Line dataKey="total_revenue" stroke="#007bff"/>
</LineChart>
</ResponsiveContainer>

</div>


<div className="card">

<h3>Category Breakdown</h3>

<ResponsiveContainer width="100%" height={300}>
<BarChart data={categories}>
<XAxis dataKey="category"/>
<YAxis/>
<Tooltip/>
<Bar dataKey="total_revenue" fill="orange"/>
</BarChart>
</ResponsiveContainer>

</div>

</div>


{/* TOP CUSTOMERS */}

<div className="card">

<h3>Top Customers</h3>

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

{customers.map((c,i)=>(
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


{/* REGION SUMMARY */}

<div className="card">

<h3>Region Summary</h3>

<table>

<thead>
<tr>
<th>Region</th>
<th>Customers</th>
<th>Orders</th>
<th>Total Revenue</th>
</tr>
</thead>

<tbody>

{regions.map((r,i)=>(
<tr key={i}>
<td>{r.region}</td>
<td>{r.customers}</td>
<td>{r.orders}</td>
<td>{r.total_revenue}</td>
</tr>
))}

</tbody>

</table>

</div>


</div>

)

}

export default App;