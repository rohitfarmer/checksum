// Purpose: To create and match checksum of files in a source and destination folder respectively.

// Import libraries
use std::env;
use std::path::Path;
// use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    let args_len = args.len();
    if args_len < 3 {
        print!("Please provide all the positional arguments.\n");
        std::process::exit(0);
    } else if &args[1] != "create" && &args[1] != "match" {
        print!("Only create or match is allowed as the first positional argument.\n");
        std::process::exit(0);
    }

    let mode = &args[1];
    let dir_path = &args[2];

    println!("Number of arguments passed {}", args_len);
    println!("Mode {}", mode);
    println!("Directory path {}", dir_path);

    if mode == "create"{
        print!("In create mode.\n");
        // let path = Path::new(dir_path, "md5_hash_at_source.json");
        let path = Path::new(dir_path);

    }

    if mode == "match"{
        print!("In match mode.\n");
    }
}
