import mysql from "mysql2/promise";
import dotenv from "dotenv";


dotenv.config();


const pool = mysql.createPool({
    host: process.env.DB_HOST_NAME,
    user: process.env.DB_USER_NAME,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
});


export default pool;
