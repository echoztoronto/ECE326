/*
 * server.rs
 *
 * Implementation of EasyDB database server
 *
 * University of Toronto
 * 2019
 */

use std::net::TcpListener;
use std::net::TcpStream;
use std::io::Write;
use std::io;
use packet::Command;
use packet::Response;
use packet::Network;
use schema::Table;
use database;
use database::Database;
use std::sync::Arc;
use std::sync::Mutex;
use std::thread;

fn single_threaded(listener: TcpListener, table_schema: Vec<Table>, verbose: bool)
{
    /* 
     * you probably need to use table_schema somewhere here or in
     * Database::new 
     */
    let mut db = vec![];
    let num_conn = Arc::new(Mutex::new(0 as i64));

    //Create a Mutex for every table
    for i in 0..table_schema.len() {
        db.push(Arc::new(Mutex::new(Database::new(table_schema))));
    }

    for stream in listener.incoming() {
        let stream = stream.unwrap();
        
        if verbose {
            println!("Connected to {}", stream.peer_addr().unwrap());
        }

        let mut db_clone = vec![];

        for i in 0..db.len() {
            db_clone.push(db[i].clone());
        }

        let num_conn_clone = num_conn.clone();

        match handle_connection(stream, db_clone, num_conn_clone) {
            Ok(()) => {
                if verbose {
                    println!("Disconnected.");
                }
            },
            Err(e) => eprintln!("Connection error: {:?}", e),
        };
    }
}

fn multi_threaded(listener: TcpListener, table_schema: Vec<Table>, verbose: bool)
{
    // TODO: implement me
    let mut db = vec![];
    let mut threads = vec![];

    //Create a Mutex for every table
    for i in 0..table_schema.len() {
        db.push(Arc::new(Mutex::new(Database::new(table_schema))));
    }

    //Number of connections to database server
    let num_conn = Arc::new(Mutex::new(0 as i64));

    for stream in listener.incoming() {
        let stream = stream.unwrap();
        
        if verbose {
            println!("Connected to {}", stream.peer_addr().unwrap());
        }
        
        let mut db_clone = vec![];

        for i in 0..db.len() {
            db_clone.push(db[i].clone());
        }

        let num_conn_clone = num_conn.clone();

        threads.push(thread::spawn(move || {
            match handle_connection(stream, db_clone, num_conn_clone) {
                Ok(()) => {
                    if verbose {
                        println!("Disconnected.");
                    }
                },
                Err(e) => eprintln!("Connection error: {:?}", e),
            };
        }));
    }

    for child in threads {
        child.join().unwrap();
    }
}

/* Sets up the TCP connection between the database client and server */
pub fn run_server(table_schema: Vec<Table>, ip_address: String, verbose: bool)
{
    let listener = match TcpListener::bind(ip_address) {
        Ok(listener) => listener,
        Err(e) => {
            eprintln!("Could not start server: {}", e);
            return;
        },
    };
    
    println!("Listening: {:?}", listener);
    
    /*
     * TODO: replace with multi_threaded
     */
    multi_threaded(listener, table_schema, verbose);
}

impl Network for TcpStream {}

/* Receive the request packet from ORM and send a response back */
fn handle_connection(mut stream: TcpStream, db: Vec<Arc<Mutex<Database>>>, num_conn: Arc<Mutex<i64>>) 
    -> io::Result<()> 
{
    /* 
     * Tells the client that the connction to server is successful.
     * TODO: respond with SERVER_BUSY when attempting to accept more than
     *       4 simultaneous clients.
     */
    
    //Check number of connections currently
    let mut total_num_conn = num_conn.lock().unwrap();

    if *total_num_conn >= 4 {
        stream.respond(&Response::Error(Response::SERVER_BUSY))?;
        return Ok(());
    }
    else {
        *total_num_conn += 1;
    }
    
    drop(total_num_conn);
    
    stream.respond(&Response::Connected)?;

    loop {
        let request = match stream.receive() {
            Ok(request) => request,
            Err(e) => {
                /* respond error */
                stream.respond(&Response::Error(Response::BAD_REQUEST))?;
                let mut total_num_conn = num_conn.lock().unwrap();
                *total_num_conn -= 1;
                return Err(e);
            },
        };
        
        /* we disconnect with client upon receiving Exit */
        if let Command::Exit = request.command {
            break;
        }

        /* Send back a response */
        let response = database::handle_request(request, db);
        
        stream.respond(&response)?;
        stream.flush()?;
    }

    let mut total_num_conn = num_conn.lock().unwrap();
    *total_num_conn -= 1;
    Ok(())
}

