import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function CategoryChart({data}){

return(

<div className="card">

<h3>Category Breakdown</h3>

<ResponsiveContainer width="100%" height={300}>
<BarChart data={data}>
<XAxis dataKey="category"/>
<YAxis/>
<Tooltip/>
<Bar dataKey="total_revenue" fill="orange"/>
</BarChart>
</ResponsiveContainer>

</div>

)

}