import { Pool } from "pg";
import dotenv from "dotenv";


dotenv.config();


const pool = new Pool({
    host: process.env.DB_HOST_NAME,
    user: process.env.DB_USER_NAME,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
});


export default pool;
