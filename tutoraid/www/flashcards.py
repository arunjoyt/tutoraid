import frappe

def get_context(context):

    # get Webpage title
    flashcards_webpage_title = frappe.get_doc("Tutor Aid Settings").flashcards_webpage_title
    if not flashcards_webpage_title:
         flashcards_webpage_title = "Flashcards"
    context.flashcards_webpage_title = flashcards_webpage_title
    # get all published quizzes
    filters = {"published": 1}
    published_topics = frappe.get_all('Topic',
                                       fields=['topic_name'],
                                       filters=filters,
                                       order_by="topic_name asc")
    published_topics = [topic['topic_name'] for topic in published_topics]
    context.published_topics = published_topics



    # Get the quiz selected by the user (if any)
    selected_topic = frappe.form_dict.get('topic')
    # on load default to the first 
    if not selected_topic:
         selected_topic = "all"
    context.selected_topic = selected_topic

    translations = []
    if selected_topic == "all":
         for topic in published_topics:
              topic_doc = frappe.get_doc("Topic", topic)
              translations.extend(topic_doc.translations)
    else:
          topic_doc = frappe.get_doc("Topic", selected_topic)
          translations = topic_doc.translations

    # Extract only language_1 and language_2
    translations = [{"question": translation.get("language_1"), "answer": translation.get("language_2")} for translation in translations]
    translations = frappe.as_json(translations)
    context.translations = translations

    context.no_cache = 1
    return context

  