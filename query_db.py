#!/usr/bin/env python3
"""
Simple script to query the test database interactively.
Usage: python query_db.py "SELECT * FROM worker LIMIT 10"
"""
import sys
import os
from dotenv import load_dotenv
from app import create_app
from app.database import get_db

# Load environment variables
load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python query_db.py 'SQL QUERY' [--test]")
        print("Example: python query_db.py 'SELECT * FROM worker LIMIT 10'")
        print("Use --test flag to query the test database")
        sys.exit(1)
    
    query = sys.argv[1]
    use_test_db = '--test' in sys.argv
    
    # Configure app to use test database if requested
    config = {}
    if use_test_db:
        config['DATABASE_URL'] = os.getenv('TEST_DATABASE_URL')
        print(f"Querying TEST database: {config['DATABASE_URL']}")
    else:
        print(f"Querying MAIN database: {os.getenv('DATABASE_URL')}")
    
    app = create_app(config if config else None)
    with app.app_context():
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                
                # If it's a SELECT query, fetch and display results
                if query.strip().upper().startswith('SELECT'):
                    results = cursor.fetchall()
                    if results:
                        # Print column names
                        colnames = [desc[0] for desc in cursor.description]
                        header = " | ".join(colnames)
                        print(header)
                        print("-" * len(header))
                        
                        # Print rows
                        for row in results:
                            # Handle dict-like rows from RealDictCursor
                            if hasattr(row, 'values'):
                                print(" | ".join(str(val) for val in row.values()))
                            else:
                                print(" | ".join(str(val) for val in row))
                        print(f"\n{len(results)} rows returned")
                    else:
                        print("No results")
                else:
                    conn.commit()
                    print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

if __name__ == "__main__":
    main()
