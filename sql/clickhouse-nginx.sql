CREATE TABLE nginx_logs
(
	timestamp DateTime, 
	client_addr String, 
	client_port UInt64, 
	client_user String, 
	request_body String, 
	request String, 
	request_length UInt64, 
	server_addr String, 
	request_time Float64, 
	server_protocol String, 
	ssl_protocol String, 
	ssl_cipher String, 
	upstream_addr String, 
	upstream_response_time Float64, 
	upstream_status UInt16, 
	http_host String, 
	http_referer String, 
	http_x_forwarded_for String, 
	http_user_agent String, 
	server_host String, 
	server_port UInt64, 
	uri String, 
	body_bytes_sent UInt64, 
	bytes_sent UInt64, 
	status UInt64
)
ENGINE = MergeTree
ORDER BY timestamp;