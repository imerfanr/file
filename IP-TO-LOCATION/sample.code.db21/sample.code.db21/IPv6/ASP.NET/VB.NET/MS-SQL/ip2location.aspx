<%@ Page Language="VB" %>

<%@ Import Namespace="System.Data.SqlClient" %>
<%@ Import Namespace="System.Numerics" %>
<%@ Import Namespace="System.Net" %>
<!DOCTYPE html>
<html lang="en">

<script runat="server">
    Const DB_HOST As String = "localhost"
    Const DB_NAME As String = "ip2location"
    Const DB_USER As String = "your_username"
    Const DB_PSWD As String = "your_password"
    Dim result As String = ""

    Private Function IPNo(ByRef ipAddress As IPAddress) As BigInteger
        Try
            Dim addrBytes() As Byte = ipAddress.GetAddressBytes()
            LittleEndian(addrBytes)

            Dim final As BigInteger

            If addrBytes.Length > 8 Then
                'IPv6
                final = System.BitConverter.ToUInt64(addrBytes, 8)
                final <<= 64
                final += System.BitConverter.ToUInt64(addrBytes, 0)
            Else
                'IPv4
                final = System.BitConverter.ToUInt32(addrBytes, 0)
            End If

            Return final
        Catch ex As Exception
            Return 0
        End Try
    End Function

    Private Sub LittleEndian(ByRef byteArr() As Byte)
        If System.BitConverter.IsLittleEndian Then
            Dim byteList As New List(Of Byte)(byteArr)
            byteList.Reverse()
            byteArr = byteList.ToArray()
        End If
    End Sub

    Sub Page_Load(Sender As Object, e As System.EventArgs)
        Dim trusted As String = "Server=" & DB_HOST & ";Database=" & DB_NAME & ";Trusted_Connection=True;"
        'Dim nontrusted As String = "Server=" & DB_HOST & ";Database=" & DB_NAME & ";User Id=" & DB_USER & ";Password=" & DB_PSWD & ";"
        Dim ip As String = ""

        If Not String.IsNullOrEmpty(Request.Form("ipAddress")) Then
            ip = Request.Form("ipAddress")
            Dim address As IPAddress = Nothing

            If IPAddress.TryParse(ip, address) AndAlso address.AddressFamily = System.Net.Sockets.AddressFamily.InterNetworkV6 Then ' IPv6
                Dim ipnum As BigInteger = IPNo(address)
                Dim ipnum2 As String = ipnum.ToString().PadLeft(39, "0")

                Using conn As SqlConnection = New SqlConnection(trusted) ' change to nontrusted if you're using username/password to connect to SQL Server
                    Dim query As String = "SELECT TOP 1 * FROM ip2location_db21_ipv6 WHERE @ipnum <= ip_to"
                    Dim cmd As SqlCommand = New SqlCommand(query, conn)
                    cmd.Parameters.Add("@ipnum", Data.SqlDbType.Char)
                    cmd.Parameters("@ipnum").Value = ipnum2
                    Try
                        conn.Open()
                        Dim reader As SqlDataReader = cmd.ExecuteReader()

                        If reader.HasRows Then
                            If reader.Read Then
                                result = "<Table Class=""table"">" & vbNewLine
                                    result &= "<tr>" & vbNewLine
                                    result &= "<th>Country Code</th>" & vbNewLine
                                    result &= "<td>" & reader.GetString(reader.GetOrdinal("country_code")) & "</td>" & vbNewLine
                                    result &= "</tr>" & vbNewLine
                                    result &= "<tr>" & vbNewLine
                                    result &= "<th>Country Name</th>" & vbNewLine
                                    result &= "<td>" & reader.GetString(reader.GetOrdinal("country_name")) & "</td>" & vbNewLine
                                    result &= "</tr>" & vbNewLine
                                    result &= "<tr>" & vbNewLine
                                    result &= "<th>Region Name</th>" & vbNewLine
                                    result &= "<td>" & reader.GetString(reader.GetOrdinal("region_name")) & "</td>" & vbNewLine
                                    result &= "</tr>" & vbNewLine
                                    result &= "<tr>" & vbNewLine
                                    result &= "<th>City Name</th>" & vbNewLine
                                    result &= "<td>" & reader.GetString(reader.GetOrdinal("city_name")) & "</td>" & vbNewLine
                                    result &= "</tr>" & vbNewLine
                                    result &= "<tr>" & vbNewLine
                                    result &= "<th>latitude</th>" & vbNewLine
                                    result &= "<td>" & reader.GetString(reader.GetOrdinal("latitude")) & "</td>" & vbNewLine
                                    result &= "</tr>" & vbNewLine
                                    result &= "<tr>" & vbNewLine
                                    result &= "<th>longitude</th>" & vbNewLine
                                    result &= "<td>" & reader.GetString(reader.GetOrdinal("longitude")) & "</td>" & vbNewLine
                                    result &= "</tr>" & vbNewLine
                                    result &= "<tr>" & vbNewLine
                                    result &= "<th>ZIP Code</th>" & vbNewLine
                                    result &= "<td>" & reader.GetString(reader.GetOrdinal("zip_code")) & "</td>" & vbNewLine
                                    result &= "</tr>" & vbNewLine
                                    result &= "<tr>" & vbNewLine
                                    result &= "<th>Time Zone</th>" & vbNewLine
                                    result &= "<td>" & reader.GetString(reader.GetOrdinal("time_zone")) & "</td>" & vbNewLine
                                    result &= "</tr>" & vbNewLine
                                    result &= "<tr>" & vbNewLine
                                    result &= "<th>IDD Code</th>" & vbNewLine
                                    result &= "<td>" & reader.GetString(reader.GetOrdinal("idd_code")) & "</td>" & vbNewLine
                                    result &= "</tr>" & vbNewLine
                                    result &= "<tr>" & vbNewLine
                                    result &= "<th>Area Code</th>" & vbNewLine
                                    result &= "<td>" & reader.GetString(reader.GetOrdinal("area_code")) & "</td>" & vbNewLine
                                    result &= "</tr>" & vbNewLine
                                    result &= "<tr>" & vbNewLine
                                    result &= "<th>Elevation</th>" & vbNewLine
                                    result &= "<td>" & reader.GetString(reader.GetOrdinal("elevation")) & "</td>" & vbNewLine
                                    result &= "</tr>" & vbNewLine
                                result &= "</table>" & vbNewLine
                            End If
                        Else
                            result = "<div class=""alert alert-info"">IP address not found.</div>"
                        End If
                    Catch ex As Exception
                        result = "<div class=""alert alert-danger"">" & ex.Message & "</div>"
                    End Try
                End Using
            Else
                result = "<div class=""alert alert-danger"">Invalid IP address.</div>"
            End If
        End If
    End Sub
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
