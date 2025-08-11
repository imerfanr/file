<%@ Page Language="C#" %>

<%@ Import Namespace="System.Data.SqlClient" %>
<%@ Import Namespace="System.Numerics" %>
<%@ Import Namespace="System.Net" %>
<!DOCTYPE html>
<html lang="en">

<script runat="server">
    const string DB_HOST = "localhost";
    const string DB_NAME = "ip2location";
    const string DB_USER = "your_username";
    const string DB_PSWD = "your_password";
    string result = "";

    private BigInteger IPNo(ref IPAddress ipAddress)
    {
        try
        {
            byte[] addrBytes = ipAddress.GetAddressBytes();
            LittleEndian(ref addrBytes);

            BigInteger final;

            if (addrBytes.Length > 8)
            {
                // IPv6
                final = System.BitConverter.ToUInt64(addrBytes, 8);
                final <<= 64;
                final += System.BitConverter.ToUInt64(addrBytes, 0);
            }
            else
                // IPv4
                final = System.BitConverter.ToUInt32(addrBytes, 0);

            return final;
        }
        catch (Exception ex)
        {
            return 0;
        }
    }

    private void LittleEndian(ref byte[] byteArr)
    {
        if (System.BitConverter.IsLittleEndian)
        {
            List<byte> byteList = new List<byte>(byteArr);
            byteList.Reverse();
            byteArr = byteList.ToArray();
        }
    }

    public void Page_Load(object Sender, System.EventArgs e)
    {
        string trusted = "Server=" + DB_HOST + ";Database=" + DB_NAME + ";Trusted_Connection=True;";
        // string nontrusted = "Server=" + DB_HOST + ";Database=" + DB_NAME + ";User Id=" + DB_USER + ";Password=" + DB_PSWD + ";";
        string ip = "";

        if (!string.IsNullOrEmpty(Request.Form["ipAddress"]))
        {
            ip = Request.Form["ipAddress"];
            IPAddress address;

            if (IPAddress.TryParse(ip, out address) && address.AddressFamily == System.Net.Sockets.AddressFamily.InterNetworkV6) // IPv6
            {
                BigInteger ipnum = IPNo(ref address);
                string ipnum2 = ipnum.ToString().PadLeft(39, '0');

                using (SqlConnection conn = new SqlConnection(trusted)) // change to nontrusted if you're using username/password to connect to SQL Server
                {
                    string query = "SELECT TOP 1 * FROM ip2location_db21_ipv6 WHERE @ipnum <= ip_to";
                    SqlCommand cmd = new SqlCommand(query, conn);
                    cmd.Parameters.Add("@ipnum", System.Data.SqlDbType.Char);
                    cmd.Parameters["@ipnum"].Value = ipnum2;
                    try
                    {
                        conn.Open();
                        SqlDataReader reader = cmd.ExecuteReader();

                        if (reader.HasRows)
                        {
                            if (reader.Read())
                            {
                                result = "<Table Class=\"table\">\n";
                                    result += "<tr>\n";
                                    result += "<th>Country Code</th>\n";
                                    result += "<td>" + reader.GetString(reader.GetOrdinal("country_code")) + "</td>\n";
                                    result += "</tr>\n";
                                    result += "<tr>\n";
                                    result += "<th>Country Name</th>\n";
                                    result += "<td>" + reader.GetString(reader.GetOrdinal("country_name")) + "</td>\n";
                                    result += "</tr>\n";
                                    result += "<tr>\n";
                                    result += "<th>Region Name</th>\n";
                                    result += "<td>" + reader.GetString(reader.GetOrdinal("region_name")) + "</td>\n";
                                    result += "</tr>\n";
                                    result += "<tr>\n";
                                    result += "<th>City Name</th>\n";
                                    result += "<td>" + reader.GetString(reader.GetOrdinal("city_name")) + "</td>\n";
                                    result += "</tr>\n";
                                    result += "<tr>\n";
                                    result += "<th>latitude</th>\n";
                                    result += "<td>" + reader.GetString(reader.GetOrdinal("latitude")) + "</td>\n";
                                    result += "</tr>\n";
                                    result += "<tr>\n";
                                    result += "<th>longitude</th>\n";
                                    result += "<td>" + reader.GetString(reader.GetOrdinal("longitude")) + "</td>\n";
                                    result += "</tr>\n";
                                    result += "<tr>\n";
                                    result += "<th>ZIP Code</th>\n";
                                    result += "<td>" + reader.GetString(reader.GetOrdinal("zip_code")) + "</td>\n";
                                    result += "</tr>\n";
                                    result += "<tr>\n";
                                    result += "<th>Time Zone</th>\n";
                                    result += "<td>" + reader.GetString(reader.GetOrdinal("time_zone")) + "</td>\n";
                                    result += "</tr>\n";
                                    result += "<tr>\n";
                                    result += "<th>IDD Code</th>\n";
                                    result += "<td>" + reader.GetString(reader.GetOrdinal("idd_code")) + "</td>\n";
                                    result += "</tr>\n";
                                    result += "<tr>\n";
                                    result += "<th>Area Code</th>\n";
                                    result += "<td>" + reader.GetString(reader.GetOrdinal("area_code")) + "</td>\n";
                                    result += "</tr>\n";
                                    result += "<tr>\n";
                                    result += "<th>Elevation</th>\n";
                                    result += "<td>" + reader.GetString(reader.GetOrdinal("elevation")) + "</td>\n";
                                    result += "</tr>\n";
                                result += "</table>\n";
                            }
                        }
                        else
                            result = "<div class=\"alert alert-info\">IP address not found.</div>";
                    }
                    catch (Exception ex)
                    {
                        result = "<div class=\"alert alert-danger\">" + ex.Message + "</div>";
                    }
                }
            }
            else
                result = "<div class=\"alert alert-danger\">Invalid IP address.</div>";
        }
    }
</script>

<head runat="server">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>IP2Location Sample</title>

    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://stackpath.bootstrapcdn.com/bootswatch/4.3.1/sandstone/bootstrap.min.css" rel="stylesheet">
</head>
<body class="py-4">
    <div class="container">
        <div class="row">
            <div class="col-sm-6">
                <h2>IP2Location Sample</h2>
                <%=result%>
                <form method="post">
                    <div class="form-group">
                        <label for="ipAddress">IP Address</label>
                        <input type="text" name="ipAddress" class="form-control">
                    </div>

                    <button type="submit" class="btn btn-success">Query</button>
                </form>
            </div>
        </div>

        <div class="row mt-5">
            <div class="col-sm-6">
                &copy; Copyright <a href="https://www.ip2location.com" target="_blank">IP2Location.com</a>.
            </div>
        </div>
    </div>
</body>

</html>
