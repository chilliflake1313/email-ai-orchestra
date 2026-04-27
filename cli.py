import argparse
from agents.reader import ReaderAgent
from agents.classifier import ClassifierAgent
from agents.executor import ExecutorAgent
from core.logger import setup_logger
from dotenv import load_dotenv
import json


def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Email AI Orchestra CLI')
    parser.add_argument('--dry-run', action='store_true', help='Preview actions without executing')
    parser.add_argument('--limit', type=int, default=50, help='Number of emails to process')
    parser.add_argument('--stats', action='store_true', help='Show statistics only')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    logger = setup_logger()
    
    if args.verbose:
        logger.setLevel('DEBUG')
    
    reader = ReaderAgent()
    
    if args.stats:
        count = reader.get_email_count()
        print(f"\n📊 Email Statistics")
        print(f"{'='*50}")
        print(f"Inbox count: {count}")
        return
    
    print(f"\n🔍 Fetching {args.limit} emails...")
    emails = reader.fetch_emails(args.limit)
    print(f"✓ Found {len(emails)} emails")
    
    print(f"\n🤖 Classifying emails using AI...")
    classifier = ClassifierAgent()
    classified = classifier.classify_batch(emails)
    print(f"✓ Classification complete")
    
    print(f"\n⚙️  Applying rules and executing actions...")
    executor = ExecutorAgent(dry_run=args.dry_run)
    results = executor.execute_actions(classified)
    summary = executor.get_summary(results)
    
    print(f"\n📋 Summary")
    print(f"{'='*50}")
    print(f"Total processed: {summary['total']}")
    print(f"Delete: {summary['delete']}")
    print(f"Archive: {summary['archive']}")
    print(f"Keep: {summary['keep']}")
    
    if args.dry_run:
        print(f"\n⚠️  DRY RUN - No actions were executed")
    else:
        print(f"Executed: {summary['executed']}")
    
    if args.verbose:
        print(f"\n📝 Detailed Results")
        print(f"{'='*50}")
        for result in results[:10]:
            print(f"\nSubject: {result['subject'][:60]}")
            print(f"Category: {result['category']}")
            print(f"Action: {result['action']}")
            print(f"Rule: {result['rule']}")
    
    print(f"\n✓ Complete\n")


if __name__ == '__main__':
    main()
