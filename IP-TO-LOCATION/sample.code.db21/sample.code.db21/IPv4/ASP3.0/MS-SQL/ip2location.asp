<%
	Dim DB_HOST = "localhost"
	Dim DB_NAME = "ip2location"
	Dim DB_USER = "your_username"
	Dim DB_PSWD = "your_password"
	Dim result = ""

	Function Dot2LongIP (ByVal DottedIP)
		Dim i, pos
		Dim PrevPos, num
		If DottedIP = "" Then
			Dot2LongIP = 0
		Else
			For i = 1 To 4
				pos = InStr(PrevPos + 1, DottedIP, ".", 1)
				If i = 4 Then 
					pos = Len(DottedIP) + 1
				End If
				num = Int(Mid(DottedIP, PrevPos + 1, pos - PrevPos - 1))
				PrevPos = pos
				Dot2LongIP = ((num Mod 256) * (256 ^ (4 - i))) + Dot2LongIP
			Next
		End If
	End Function

	If Not Request.Form("ipAddress") = "" Then
		ipaddress = Request.Form("ipAddress")
		
		Dim conn, rs, sql, trusted, nontrusted
		trusted = "Driver={SQL Server Native Client 11.0};Server=" & DB_HOST & ";Database=" & DB_NAME & ";Trusted_Connection=yes;"
		' nontrusted = "Driver={SQL Server Native Client 11.0};Server=" & DB_HOST & ";Database=" & DB_NAME & ";Uid=" & DB_USER & ";Pwd=" & DB_PSWD & ";"
		
		Set conn = Server.CreateObject("ADODB.Connection")
		conn.open trusted ' change to nontrusted if you're using username/password to connect to SQL Server
		
		ipno = Dot2LongIP(ipaddress)
		
		sql = "SELECT TOP 1 * FROM ip2location_db21 WHERE " & ipno & " <= ip_to"
		
		Set rs = conn.execute(sql)
		
		If Not rs.EOF Then
			result = "<Table Class=""table"">" & vbCrLf
			result &= "<tr>" & vbCrLf
			result &= "<th>Country Code</th>" & vbCrLf
			result &= "<td>" & rs("country_code") & "</td>" & vbCrLf
			result &= "</tr>" & vbCrLf
			result &= "<tr>" & vbCrLf
			result &= "<th>Country Name</th>" & vbCrLf
			result &= "<td>" & rs("country_name") & "</td>" & vbCrLf
			result &= "</tr>" & vbCrLf
			result &= "<tr>" & vbCrLf
			result &= "<th>Region Name</th>" & vbCrLf
			result &= "<td>" & rs("region_name") & "</td>" & vbCrLf
			result &= "</tr>" & vbCrLf
			result &= "<tr>" & vbCrLf
			result &= "<th>City Name</th>" & vbCrLf
			result &= "<td>" & rs("city_name") & "</td>" & vbCrLf
			result &= "</tr>" & vbCrLf
			result &= "<tr>" & vbCrLf
			result &= "<th>latitude</th>" & vbCrLf
			result &= "<td>" & rs("latitude") & "</td>" & vbCrLf
			result &= "</tr>" & vbCrLf
			result &= "<tr>" & vbCrLf
			result &= "<th>longitude</th>" & vbCrLf
			result &= "<td>" & rs("longitude") & "</td>" & vbCrLf
			result &= "</tr>" & vbCrLf
			result &= "<tr>" & vbCrLf
			result &= "<th>ZIP Code</th>" & vbCrLf
			result &= "<td>" & rs("zip_code") & "</td>" & vbCrLf
			result &= "</tr>" & vbCrLf
			result &= "<tr>" & vbCrLf
			result &= "<th>Time Zone</th>" & vbCrLf
			result &= "<td>" & rs("time_zone") & "</td>" & vbCrLf
			result &= "</tr>" & vbCrLf
			result &= "<tr>" & vbCrLf
			result &= "<th>IDD Code</th>" & vbCrLf
			result &= "<td>" & rs("idd_code") & "</td>" & vbCrLf
			result &= "</tr>" & vbCrLf
			result &= "<tr>" & vbCrLf
			result &= "<th>Area Code</th>" & vbCrLf
			result &= "<td>" & rs("area_code") & "</td>" & vbCrLf
			result &= "</tr>" & vbCrLf
			result &= "<tr>" & vbCrLf
			result &= "<th>Elevation</th>" & vbCrLf
			result &= "<td>" & rs("elevation") & "</td>" & vbCrLf
			result &= "</tr>" & vbCrLf
			result &= "</table>" & vbCrLf
		Else
			result = "<div class=""alert alert-info"">IP address not found.</div>"
		End If
		rs.close
		Set rs = Nothing
		conn.close
		Set conn = Nothing
	End if

%>
<!DOCTYPE html>
<html lang="en">
<head>
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
