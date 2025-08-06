import { useEffect, useState } from "react";
import axios from "axios";

function Templates() {
    const [templates, setTemplates] = useState([])
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchTemplates();
    }, []);

    const fetchTemplates = async () => {
        try {
            const res = await axios.get("http://localhost:8000/templates");
            setTemplates(res.data);
            setLoading(false);
        } catch (err) {
            console.error("Ошибка при получении шаблонов:", err);
        }
    };

    const handleChange = (index, newValue) => {
        const updated = [...templates];
        updated[index].content = newValue;
        setTemplates(updated);
    };

    const handleSave = async (template) => {
        try {
            await axios.put(`http://localhost:8000/templates/${template.id}`, {
                content: template.content,
            });
            alert("✅ Сохранено!")
        } catch (err) {
            alert("Ошибка при сохранении")
        }
    };

    if (loading) return <p>Загрузка шаблонов...</p>

    return (
        <div className="m-12">
            <h2 className="hd p-0">Редактирование шаблонов</h2>
            {templates.map((template, index) => (
                <div key={template.id} className="my-6">
                    <h3 className="block mb-2 text-lg font-medium">{template.name}</h3>
                    <textarea className="block p-2.5 w-full text-base text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500" value={template.content} onChange={(e) => handleChange(index, e.target.value)} rows={4} />
                    <button className="my-4 inline-flex items-center py-2.5 px-4 text-xs font-medium text-center text-white bg-blue-700 rounded-lg focus:ring-4 focus:ring-blue-200 dark:focus:ring-blue-900 hover:bg-blue-800" onClick={() => handleSave(template)}>Сохранить</button>
                </div>
            ))}
            <button className="py-2.5 px-5 me-2 mb-2 flex items-center text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-4">
  <path strokeLinecap="round" strokeLinejoin="round" d="m18.75 4.5-7.5 7.5 7.5 7.5m-6-15L5.25 12l7.5 7.5" />
</svg>

                <a href="/" className="pl-2">Назад в главный меню</a>
            </button>
        </div>
    )
}

export default Templates