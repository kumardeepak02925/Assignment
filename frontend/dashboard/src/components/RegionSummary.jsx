export default function RegionSummary({data}){

    return(
    
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
    
    {data.map((r,i)=>(
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
    
    )
    
    }