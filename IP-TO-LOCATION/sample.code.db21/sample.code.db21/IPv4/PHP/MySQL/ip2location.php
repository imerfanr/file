<?php
define('DB_HOST', 'localhost');
define('DB_NAME', 'ip2location');
define('DB_USER', 'root');
define('DB_PSWD', '');

$result = '';
if (isset($_POST['ipAddress'])) {
	try {
		// Initial MySQL connection
		$db = new PDO('mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8', DB_USER, DB_PSWD);
		$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

		$st = $db->prepare('SELECT * FROM `ip2location_db21` WHERE INET_ATON(:ip) <= `ip_to` LIMIT 1');
		$st->execute([
			':ip' => $_POST['ipAddress'],
		]);

		if ($st->rowCount() == 0) {
			$result = '<div class="alert alert-info">IP address not found.</div>';
		} else {
			$row = $st->fetch(PDO::FETCH_ASSOC);

			$result = '
			<table class="table">
				<tr>
					<th>Country Code</th>
					<td>' . $row['country_code'] . '</td>
				</tr>
				<tr>
					<th>Country Name</th>
					<td>' . $row['country_name'] . '</td>
				</tr>
				<tr>
					<th>Region Name</th>
					<td>' . $row['region_name'] . '</td>
				</tr>
				<tr>
					<th>City Name</th>
					<td>' . $row['city_name'] . '</td>
				</tr>
				<tr>
					<th>latitude</th>
					<td>' . $row['latitude'] . '</td>
				</tr>
				<tr>
					<th>longitude</th>
					<td>' . $row['longitude'] . '</td>
				</tr>
				<tr>
					<th>ZIP Code</th>
					<td>' . $row['zip_code'] . '</td>
				</tr>
				<tr>
					<th>Time Zone</th>
					<td>' . $row['time_zone'] . '</td>
				</tr>
				<tr>
					<th>IDD Code</th>
					<td>' . $row['idd_code'] . '</td>
				</tr>
				<tr>
					<th>Area Code</th>
					<td>' . $row['area_code'] . '</td>
				</tr>
				<tr>
					<th>Elevation</th>
					<td>' . $row['elevation'] . '</td>
				</tr>
			</table>';
		}
	} catch (PDOException $e) {
		$result = '<div class="alert alert-danger">' . $e->getMessage() . '</div>';
	}
}

?>

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
					<?php echo $result; ?>
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