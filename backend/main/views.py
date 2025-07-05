from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.conf import settings
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from .wordle_ai import EntropyAI, WordList, LetterInformation
import random
import json
import os
from difflib import get_close_matches
from .hnn_ai import Text_Processor 
from django.views.generic import TemplateView

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"
    

@ensure_csrf_cookie
def set_csrf(request):
    return JsonResponse({'message': 'CSRF cookie set'})

def hello_world(request):
    return JsonResponse({"message": "Hello World!"})

class FrontendAppView(View):
    def get(self, request):
        index_path = os.path.join(settings.BASE_DIR, 'frontend_dist', 'index.html')
        try:
            with open(index_path, 'r') as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponseNotFound("React build not found. Please run `npm run build`.")

@csrf_exempt 
def word_correction_api(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            current_guess = body.get('currentGuess', '').lower()
            print('here in views', current_guess)
            if not current_guess or len(current_guess) != 5:
                return JsonResponse({'error': 'Invalid answer'}, status=400)
                    
            base_dir = os.path.dirname(os.path.abspath(__file__))
            wordlist_path_common_words = os.path.join(base_dir, 'assets', 'shuffled_real_wordles.txt')
            common_words = WordList(wordlist_path_common_words).get_list_copy()
                
            # Get top 6 similar words
            top_similar_words = get_close_matches(current_guess, common_words, n=5, cutoff=0.8)

            if len(top_similar_words) == 0:
                
                return JsonResponse({
                    'current_guess': current_guess,
                    'corrected_word': current_guess
                })
            
            else:
                words_upper = [word.upper() for word in top_similar_words]

                txt_processor = Text_Processor(words_upper)

                word_pair = txt_processor.process_word(current_guess)
                input_word = word_pair[0]
                output_word = word_pair[1]

                return JsonResponse({
                    'current_guess': input_word,
                    'corrected_word': output_word
                })
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

            
    



@csrf_exempt  # Allow POST from React without CSRF token for now
def wordle_solver_api(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            answer = body.get('answer', '').lower()
            print('here in views', answer)
            if not answer or len(answer) != 5:
                return JsonResponse({'error': 'Invalid answer'}, status=400)


            # Load word list
            base_dir = os.path.dirname(os.path.abspath(__file__))
            wordlist_path_all_words = os.path.join(base_dir, 'assets', 'combined_wordlist.txt')
            all_words = WordList(wordlist_path_all_words).get_list_copy()
            # print("here", all_words)
          

            # wordlist_path_common_words = os.path.join(base_dir, 'assets', 'shuffled_real_wordles.txt')
            # common_words = WordList(wordlist_path_common_words).get_list_copy()
          
          
           
            # Run Wordle AI
            ai = EntropyAI(all_words)
            
            history = []
            max_attempts = 6
            for attempt in range(max_attempts):
                guess = ai.guess(history)
          
                feedback = ai.get_feedback(guess, answer)
                
                history.append((guess, feedback))
                if guess == answer:
                    break

            # Format response
            formatted_history = []
            for guess, feedback in history:
                formatted_history.append({
                    'guess': guess,
                    'feedback': [f.name for f in feedback]
                })

            return JsonResponse({
                'attempts': len(formatted_history),
                'history': formatted_history
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'POST request required'}, status=405)

