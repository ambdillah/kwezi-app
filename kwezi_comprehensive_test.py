#!/usr/bin/env python3
"""
🎯 TESTS COMPLETS AVANT LANCEMENT - Application Kwezi
Comprehensive Backend Testing for Kwezi Application Launch

Tests all critical functionality as specified in the French review request:
1. 🎮 Games functionality (4 games) - HIGH PRIORITY
2. 💳 Stripe payment system - CRITICAL PRIORITY  
3. 📄 Legal documents accessibility - MEDIUM PRIORITY
4. 🔧 General API health and vocabulary - MEDIUM PRIORITY

Application Kwezi: Apprentissage du Shimaoré et Kibouchi
- 636 mots dans 16 catégories
- 4 jeux d'apprentissage
- Système freemium (250 mots gratuits, premium à 2,90€/mois via Stripe)
- Documents légaux: privacy-policy, terms-of-sale, mentions-legales
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple
import sys

# Configuration
BACKEND_URL = "https://mayotte-learn-3.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

class KweziComprehensiveTester:
    def __init__(self):
        self.results = {
            "games": {},
            "stripe": {},
            "legal_docs": {},
            "general": {},
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0,
                "critical_failures": []
            }
        }
        self.test_user_id = f"test_user_{int(time.time())}"
        
    def log_test(self, category: str, test_name: str, status: str, details: str = "", response_data: Any = None):
        """Log test results with comprehensive tracking"""
        self.results[category][test_name] = {
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.results["summary"]["total_tests"] += 1
        
        if status == "✅ PASS":
            self.results["summary"]["passed"] += 1
        elif status == "❌ FAIL":
            self.results["summary"]["failed"] += 1
            # Track critical failures
            if category in ["games", "stripe"]:
                self.results["summary"]["critical_failures"].append(f"{category}: {test_name}")
        elif status == "⚠️ WARNING":
            self.results["summary"]["warnings"] += 1
            
        print(f"{status} {test_name}: {details}")

    def test_backend_health(self) -> bool:
        """Test backend health and MongoDB connection"""
        print("\n🔍 TESTING BACKEND HEALTH...")
        
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "status" in data:
                    self.log_test("general", "Backend Health Check", "✅ PASS", 
                                f"Backend responding: {data.get('message', '')}")
                    return True
                else:
                    self.log_test("general", "Backend Health Check", "⚠️ WARNING", 
                                "Backend responding but unexpected format")
                    return True
            else:
                self.log_test("general", "Backend Health Check", "❌ FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("general", "Backend Health Check", "❌ FAIL", f"Connection error: {str(e)}")
            return False

    def test_vocabulary_api(self) -> Tuple[bool, int]:
        """Test main vocabulary API - should return 636 words as specified"""
        print("\n📚 TESTING VOCABULARY API...")
        
        try:
            response = requests.get(f"{API_BASE}/words", timeout=15)
            if response.status_code == 200:
                words = response.json()
                word_count = len(words)
                
                if word_count >= 636:
                    self.log_test("general", "Vocabulary Word Count", "✅ PASS", 
                                f"Found {word_count} words (≥636 expected)")
                    success = True
                else:
                    self.log_test("general", "Vocabulary Word Count", "⚠️ WARNING", 
                                f"Found {word_count} words (<636 expected)")
                    success = False
                
                # Test word structure
                if word_count > 0:
                    sample_word = words[0]
                    required_fields = ["french", "shimaore", "kibouchi", "category"]
                    missing_fields = [field for field in required_fields if field not in sample_word]
                    
                    if not missing_fields:
                        self.log_test("general", "Word Structure Validation", "✅ PASS", 
                                    "All required fields present")
                    else:
                        self.log_test("general", "Word Structure Validation", "❌ FAIL", 
                                    f"Missing fields: {missing_fields}")
                        success = False
                
                return success, word_count
            else:
                self.log_test("general", "Vocabulary API", "❌ FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False, 0
        except Exception as e:
            self.log_test("general", "Vocabulary API", "❌ FAIL", f"Error: {str(e)}")
            return False, 0

    def test_construire_phrases_game(self) -> bool:
        """Test 'Construire des phrases' game - GET /api/sentences?limit=10"""
        print("\n🔤 Testing Construire des phrases game...")
        
        try:
            # Test basic sentences endpoint
            response = requests.get(f"{API_BASE}/sentences?limit=10", timeout=10)
            if response.status_code == 200:
                sentences = response.json()
                
                if len(sentences) == 10:
                    self.log_test("games", "Construire Phrases - Count", "✅ PASS", 
                                f"Retrieved exactly 10 sentences")
                    
                    # Validate sentence structure
                    if sentences:
                        sample_sentence = sentences[0]
                        required_fields = ["french", "shimaore", "kibouchi", "shimaore_words", "kibouchi_words"]
                        missing_fields = [field for field in required_fields if field not in sample_sentence]
                        
                        if not missing_fields:
                            self.log_test("games", "Construire Phrases - Structure", "✅ PASS", 
                                        "Sentences have all required fields")
                        else:
                            self.log_test("games", "Construire Phrases - Structure", "❌ FAIL", 
                                        f"Missing fields: {missing_fields}")
                            return False
                        
                        # Check if words are arrays
                        shimaore_words = sample_sentence.get("shimaore_words", [])
                        kibouchi_words = sample_sentence.get("kibouchi_words", [])
                        
                        if isinstance(shimaore_words, list) and isinstance(kibouchi_words, list):
                            self.log_test("games", "Construire Phrases - Word Arrays", "✅ PASS", 
                                        "Word arrays properly formatted")
                        else:
                            self.log_test("games", "Construire Phrases - Word Arrays", "❌ FAIL", 
                                        "Word arrays not properly formatted")
                            return False
                    
                    # Test variety - check for different verbs
                    verbs_found = set()
                    for sentence in sentences:
                        # Try to identify verbs in sentences (basic heuristic)
                        french_text = sentence.get("french", "").lower()
                        for verb in ["voir", "aller", "faire", "être", "avoir", "dire", "venir", "donner"]:
                            if verb in french_text:
                                verbs_found.add(verb)
                    
                    if len(verbs_found) >= 5:
                        self.log_test("games", "Construire Phrases - Verb Variety", "✅ PASS", 
                                    f"Found {len(verbs_found)} different verbs")
                    else:
                        self.log_test("games", "Construire Phrases - Verb Variety", "⚠️ WARNING", 
                                    f"Limited verb variety: {len(verbs_found)} verbs")
                    
                    return True
                
                elif len(sentences) > 0:
                    self.log_test("games", "Construire Phrases - Count", "⚠️ WARNING", 
                                f"Retrieved {len(sentences)} sentences (expected 10)")
                    return True
                else:
                    self.log_test("games", "Construire Phrases - Count", "❌ FAIL", 
                                "No sentences returned")
                    return False
            else:
                self.log_test("games", "Construire Phrases API", "❌ FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("games", "Construire Phrases API", "❌ FAIL", f"Error: {str(e)}")
            return False

    def test_quiz_mayotte(self) -> bool:
        """Test Quiz Mayotte - vocabulary-based quiz functionality"""
        print("\n🏝️ Testing Quiz Mayotte...")
        
        try:
            response = requests.get(f"{API_BASE}/words", timeout=10)
            if response.status_code == 200:
                words = response.json()
                
                # Check if we have enough words for quiz generation (26 questions expected)
                if len(words) >= 26:
                    self.log_test("games", "Quiz Mayotte - Word Base", "✅ PASS", 
                                f"Sufficient words ({len(words)}) for 26 quiz questions")
                else:
                    self.log_test("games", "Quiz Mayotte - Word Base", "⚠️ WARNING", 
                                f"Limited words ({len(words)}) for quiz variety")
                    return False
                
                # Check categories for quiz diversity
                categories = set(word.get("category", "") for word in words if word.get("category"))
                if len(categories) >= 4:
                    self.log_test("games", "Quiz Mayotte - Categories", "✅ PASS", 
                                f"Good category diversity: {len(categories)} categories")
                else:
                    self.log_test("games", "Quiz Mayotte - Categories", "⚠️ WARNING", 
                                f"Limited categories: {len(categories)}")
                
                # Check word completeness for quiz questions
                complete_words = [w for w in words if w.get("french") and w.get("shimaore") and w.get("kibouchi")]
                completeness_rate = len(complete_words) / len(words) * 100 if words else 0
                
                if completeness_rate >= 90:
                    self.log_test("games", "Quiz Mayotte - Word Completeness", "✅ PASS", 
                                f"Word completeness: {completeness_rate:.1f}%")
                    return True
                else:
                    self.log_test("games", "Quiz Mayotte - Word Completeness", "⚠️ WARNING", 
                                f"Word completeness: {completeness_rate:.1f}%")
                    return False
            else:
                self.log_test("games", "Quiz Mayotte API", "❌ FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("games", "Quiz Mayotte API", "❌ FAIL", f"Error: {str(e)}")
            return False

    def test_vocabulary_quiz(self) -> bool:
        """Test Vocabulary Quiz - GET /api/words?category={category}"""
        print("\n📖 Testing Vocabulary Quiz...")
        
        try:
            # First get available categories
            response = requests.get(f"{API_BASE}/words", timeout=10)
            if response.status_code == 200:
                words = response.json()
                categories = list(set(word.get("category", "") for word in words if word.get("category")))
                
                if categories:
                    # Test category filtering with first available category
                    test_category = categories[0]
                    cat_response = requests.get(f"{API_BASE}/words?category={test_category}", timeout=10)
                    
                    if cat_response.status_code == 200:
                        cat_words = cat_response.json()
                        
                        # Verify all words belong to the category
                        correct_category = all(word.get("category") == test_category for word in cat_words)
                        
                        if correct_category and len(cat_words) > 0:
                            self.log_test("games", "Vocabulary Quiz - Category Filter", "✅ PASS", 
                                        f"Category '{test_category}' filtering works ({len(cat_words)} words)")
                        else:
                            self.log_test("games", "Vocabulary Quiz - Category Filter", "❌ FAIL", 
                                        f"Category filtering failed for '{test_category}'")
                            return False
                        
                        # Check if words have shimaoré and kibouchi for quiz questions
                        complete_words = [w for w in cat_words if w.get("shimaore") and w.get("kibouchi")]
                        if len(complete_words) == len(cat_words):
                            self.log_test("games", "Vocabulary Quiz - Translations", "✅ PASS", 
                                        "All words have shimaoré and kibouchi translations")
                            return True
                        else:
                            self.log_test("games", "Vocabulary Quiz - Translations", "⚠️ WARNING", 
                                        f"{len(complete_words)}/{len(cat_words)} words have complete translations")
                            return len(complete_words) > 0
                    else:
                        self.log_test("games", "Vocabulary Quiz - Category API", "❌ FAIL", 
                                    f"HTTP {cat_response.status_code}")
                        return False
                else:
                    self.log_test("games", "Vocabulary Quiz - Categories", "❌ FAIL", 
                                "No categories found")
                    return False
            else:
                self.log_test("games", "Vocabulary Quiz API", "❌ FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("games", "Vocabulary Quiz API", "❌ FAIL", f"Error: {str(e)}")
            return False

    def test_conjugation_game(self) -> bool:
        """Test Conjugation Game - uses /api/sentences for conjugation practice"""
        print("\n🔄 Testing Conjugation Game...")
        
        try:
            response = requests.get(f"{API_BASE}/sentences", timeout=10)
            if response.status_code == 200:
                sentences = response.json()
                
                if len(sentences) > 0:
                    self.log_test("games", "Conjugation Game - Sentences Available", "✅ PASS", 
                                f"Found {len(sentences)} sentences for conjugation practice")
                    
                    # Check if sentences have conjugation-relevant fields
                    sample_sentence = sentences[0]
                    conjugation_fields = ["french", "shimaore", "kibouchi"]
                    has_conjugation_fields = all(field in sample_sentence for field in conjugation_fields)
                    
                    if has_conjugation_fields:
                        self.log_test("games", "Conjugation Game - Structure", "✅ PASS", 
                                    "Sentences have required conjugation fields")
                        return True
                    else:
                        self.log_test("games", "Conjugation Game - Structure", "❌ FAIL", 
                                    "Sentences missing conjugation fields")
                        return False
                else:
                    self.log_test("games", "Conjugation Game - Sentences Available", "❌ FAIL", 
                                "No sentences available for conjugation")
                    return False
            else:
                self.log_test("games", "Conjugation Game API", "❌ FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("games", "Conjugation Game API", "❌ FAIL", f"Error: {str(e)}")
            return False

    def test_stripe_checkout(self) -> bool:
        """Test POST /api/create-checkout-session"""
        print("\n💰 Testing Stripe Checkout Session Creation...")
        
        try:
            payload = {"user_id": self.test_user_id}
            response = requests.post(f"{API_BASE}/create-checkout-session", 
                                   json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if "session_url" in data and "session_id" in data:
                    session_url = data["session_url"]
                    if "stripe.com" in session_url or "checkout.stripe.com" in session_url:
                        self.log_test("stripe", "Checkout Session Creation", "✅ PASS", 
                                    "Valid Stripe checkout session created")
                        return True
                    else:
                        self.log_test("stripe", "Checkout Session Creation", "⚠️ WARNING", 
                                    f"Session URL doesn't appear to be Stripe: {session_url}")
                        return False
                else:
                    self.log_test("stripe", "Checkout Session Creation", "❌ FAIL", 
                                f"Missing session_url or session_id in response")
                    return False
            else:
                self.log_test("stripe", "Checkout Session Creation", "❌ FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("stripe", "Checkout Session Creation", "❌ FAIL", f"Error: {str(e)}")
            return False

    def test_stripe_webhook(self) -> bool:
        """Test POST /api/stripe-webhook"""
        print("\n🔗 Testing Stripe Webhook...")
        
        try:
            headers = {"stripe-signature": "test"}
            payload = {"type": "test_event"}
            
            response = requests.post(f"{API_BASE}/stripe-webhook", 
                                   json=payload, headers=headers, timeout=10)
            
            # Webhook should be accessible (may return error due to invalid signature, but that's expected)
            if response.status_code in [200, 400, 401]:
                self.log_test("stripe", "Webhook Endpoint", "✅ PASS", 
                            f"Webhook endpoint accessible (HTTP {response.status_code})")
                return True
            else:
                self.log_test("stripe", "Webhook Endpoint", "❌ FAIL", 
                            f"Webhook endpoint not accessible: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("stripe", "Webhook Endpoint", "❌ FAIL", f"Error: {str(e)}")
            return False

    def test_stripe_portal(self) -> bool:
        """Test POST /api/create-portal-session"""
        print("\n🏪 Testing Stripe Customer Portal...")
        
        try:
            payload = {"user_id": self.test_user_id}
            response = requests.post(f"{API_BASE}/create-portal-session", 
                                   json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if "url" in data:
                    portal_url = data["url"]
                    if "stripe.com" in portal_url or "billing.stripe.com" in portal_url:
                        self.log_test("stripe", "Customer Portal", "✅ PASS", 
                                    "Valid Stripe customer portal URL returned")
                        return True
                    else:
                        self.log_test("stripe", "Customer Portal", "⚠️ WARNING", 
                                    f"Portal URL doesn't appear to be Stripe: {portal_url}")
                        return False
                else:
                    self.log_test("stripe", "Customer Portal", "❌ FAIL", 
                                f"Missing 'url' in response")
                    return False
            else:
                self.log_test("stripe", "Customer Portal", "❌ FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("stripe", "Customer Portal", "❌ FAIL", f"Error: {str(e)}")
            return False

    def test_legal_documents(self) -> bool:
        """Test legal documents accessibility"""
        print("\n📄 TESTING LEGAL DOCUMENTS...")
        
        legal_docs = [
            ("privacy-policy", "Privacy Policy"),
            ("terms-of-sale", "Terms of Sale"), 
            ("mentions-legales", "Mentions Légales")
        ]
        
        all_success = True
        for doc_path, doc_name in legal_docs:
            try:
                response = requests.get(f"{BACKEND_URL}/{doc_path}", timeout=10)
                
                if response.status_code == 200:
                    content = response.text
                    if len(content) > 100:  # Reasonable content length
                        self.log_test("legal_docs", f"{doc_name} Accessibility", "✅ PASS", 
                                    f"Document accessible ({len(content)} characters)")
                    else:
                        self.log_test("legal_docs", f"{doc_name} Accessibility", "⚠️ WARNING", 
                                    f"Document accessible but short content ({len(content)} chars)")
                        all_success = False
                else:
                    self.log_test("legal_docs", f"{doc_name} Accessibility", "❌ FAIL", 
                                f"HTTP {response.status_code}")
                    all_success = False
            except Exception as e:
                self.log_test("legal_docs", f"{doc_name} Accessibility", "❌ FAIL", f"Error: {str(e)}")
                all_success = False
        
        return all_success

    def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all comprehensive tests for Kwezi application launch"""
        print("🚀 STARTING COMPREHENSIVE KWEZI BACKEND TESTING")
        print("=" * 70)
        print("🎯 Application Kwezi - Tests complets avant lancement")
        print("📚 636 mots | 🎮 4 jeux | 💳 Système freemium | 📄 Documents légaux")
        print("=" * 70)
        
        start_time = time.time()
        
        # 1. GENERAL TESTS (Foundation)
        print("\n🔧 GENERAL API TESTS...")
        backend_healthy = self.test_backend_health()
        vocab_success, word_count = self.test_vocabulary_api()
        
        # 2. GAMES TESTS (HIGH PRIORITY)
        print("\n🎮 GAMES FUNCTIONALITY TESTS (HIGH PRIORITY)...")
        games_results = {
            "construire_phrases": self.test_construire_phrases_game(),
            "quiz_mayotte": self.test_quiz_mayotte(),
            "vocabulary_quiz": self.test_vocabulary_quiz(),
            "conjugation_game": self.test_conjugation_game()
        }
        
        # 3. STRIPE TESTS (CRITICAL PRIORITY)
        print("\n💳 STRIPE PAYMENT SYSTEM TESTS (CRITICAL PRIORITY)...")
        stripe_results = {
            "checkout": self.test_stripe_checkout(),
            "webhook": self.test_stripe_webhook(),
            "portal": self.test_stripe_portal()
        }
        
        # 4. LEGAL DOCUMENTS (MEDIUM PRIORITY)
        print("\n📄 LEGAL DOCUMENTS TESTS (MEDIUM PRIORITY)...")
        legal_success = self.test_legal_documents()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Generate comprehensive summary
        return self.generate_launch_readiness_report(duration, {
            "backend_healthy": backend_healthy,
            "vocab_success": vocab_success,
            "word_count": word_count,
            "games_results": games_results,
            "stripe_results": stripe_results,
            "legal_success": legal_success
        })

    def generate_launch_readiness_report(self, duration: float, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive launch readiness report"""
        print("\n" + "=" * 70)
        print("📊 KWEZI APPLICATION LAUNCH READINESS REPORT")
        print("=" * 70)
        
        summary = self.results["summary"]
        print(f"⏱️  Test Duration: {duration:.2f} seconds")
        print(f"📈 Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"⚠️  Warnings: {summary['warnings']}")
        
        success_rate = (summary['passed'] / summary['total_tests'] * 100) if summary['total_tests'] > 0 else 0
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        # CRITICAL LAUNCH BLOCKERS ASSESSMENT
        print("\n🎯 LAUNCH READINESS ASSESSMENT:")
        
        critical_blockers = []
        
        # Check Games (HIGH PRIORITY)
        games_failed = sum(1 for result in test_results["games_results"].values() if not result)
        if games_failed > 0:
            failed_games = [game for game, success in test_results["games_results"].items() if not success]
            critical_blockers.append(f"🎮 Games not functional: {', '.join(failed_games)}")
        
        # Check Stripe (CRITICAL PRIORITY)
        stripe_failed = sum(1 for result in test_results["stripe_results"].values() if not result)
        if stripe_failed > 0:
            failed_stripe = [feature for feature, success in test_results["stripe_results"].items() if not success]
            critical_blockers.append(f"💳 Stripe not operational: {', '.join(failed_stripe)}")
        
        # Check Legal Documents (MEDIUM PRIORITY - but required for launch)
        if not test_results["legal_success"]:
            critical_blockers.append("📄 Legal documents inaccessible")
        
        # Check Vocabulary Count (should be 636+)
        if test_results["word_count"] < 636:
            critical_blockers.append(f"📚 Insufficient vocabulary: {test_results['word_count']}/636 words")
        
        # FINAL LAUNCH DECISION
        if not critical_blockers:
            print("🟢 APPLICATION READY FOR LAUNCH")
            print("   ✅ All critical systems operational")
            print("   ✅ Games functionality verified")
            print("   ✅ Stripe payment system working")
            print("   ✅ Legal documents accessible")
            print("   ✅ Vocabulary complete (636+ words)")
            launch_ready = True
        else:
            print("🔴 CRITICAL BLOCKERS IDENTIFIED - LAUNCH NOT RECOMMENDED")
            for blocker in critical_blockers:
                print(f"   ❌ {blocker}")
            launch_ready = False
        
        # DETAILED RESULTS BY PRIORITY
        print("\n📋 DETAILED RESULTS BY PRIORITY:")
        
        # CRITICAL PRIORITY - Stripe
        print(f"\n💳 STRIPE PAYMENT SYSTEM (CRITICAL):")
        for feature, success in test_results["stripe_results"].items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"  {status} {feature.replace('_', ' ').title()}")
        
        # HIGH PRIORITY - Games
        print(f"\n🎮 GAMES FUNCTIONALITY (HIGH PRIORITY):")
        for game, success in test_results["games_results"].items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"  {status} {game.replace('_', ' ').title()}")
        
        # MEDIUM PRIORITY - Legal & General
        print(f"\n📄 LEGAL DOCUMENTS (MEDIUM PRIORITY):")
        legal_status = "✅ PASS" if test_results["legal_success"] else "❌ FAIL"
        print(f"  {legal_status} Legal Documents Accessibility")
        
        print(f"\n🔧 GENERAL API (MEDIUM PRIORITY):")
        backend_status = "✅ PASS" if test_results["backend_healthy"] else "❌ FAIL"
        vocab_status = "✅ PASS" if test_results["vocab_success"] else "❌ FAIL"
        print(f"  {backend_status} Backend Health")
        print(f"  {vocab_status} Vocabulary API ({test_results['word_count']} words)")
        
        # Save detailed results
        report_data = {
            "launch_ready": launch_ready,
            "success_rate": success_rate,
            "critical_blockers": critical_blockers,
            "test_duration": duration,
            "detailed_results": self.results,
            "summary": summary
        }
        
        with open("/app/kwezi_launch_readiness_report.json", "w") as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\n💾 Detailed report saved to: /app/kwezi_launch_readiness_report.json")
        
        return report_data

if __name__ == "__main__":
    print("🎯 Kwezi Application - Comprehensive Backend Testing")
    print("📱 Apprentissage du Shimaoré et Kibouchi")
    print("🚀 Tests complets avant lancement\n")
    
    tester = KweziComprehensiveTester()
    report = tester.run_comprehensive_tests()
    
    # Exit with appropriate code
    sys.exit(0 if report["launch_ready"] else 1)