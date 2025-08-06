import { useEffect, useState } from "react";
import axios from "axios"

function Invites() {
    const [invites, setInvites] = useState([])
    const [loading, setLoading] = useState(true)
    const [filterUserId, setFilterUserId] = useState("")
    const [filterDate, setFilterDate] = useState("")

    useEffect(() => {
        fetchInvites();
    }, [])

    const fetchInvites = async () => {
        try {
            const params = {};
            if (filterUserId) params.user_id = filterUserId;
            if (filterDate) params.date = filterDate;

            const res = await axios.get("http://localhost:8000/invites", { params });
            setInvites(res.data);
            setLoading(false);
        } catch (err) {
            console.error("Ошибка при получении шаблонов:", err)
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Удалить это приглашение?")) return;
        try {
            await axios.delete(`http://localhost:8000/invites/${id}`);
            fetchInvites();
        } catch (err) {
            console.error("Ошибка при удалении:", err)
        }
    }
    if (loading) return  <p>Загрузка списка...</p>

    return (
        <div className="m-12">
            <h2 className="hd p-0">Список подтверждений</h2>
            <div className="flex gap-4 mb-4">
                <input type="text" placeholder="Фильтр по User ID" className="border rounded p-2" value={filterUserId} onChange={(e) => setFilterUserId(e.target.value)} />
                <input type="date" className="border rounded p-2" value={filterDate} onChange={(e) => setFilterDate(e.target.value)} />
                <button className="bg-gray-700 text-white px-4 rounded" onClick={fetchInvites}>Применить фильтр</button>
            </div>
            <div className="relative overflow-x-auto my-4">
                <table className="w-full text-base text-left text-gray-500 dark:text-gray-400 rtl:text-right">
                    <thead className="text-base text-gray-700 uppercase dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                            <th scope="col" className="px-6 py-3">ID</th>
                            <th scope="col" className="px-6 py-3">User ID</th>
                            <th scope="col" className="px-6 py-3">Дата и время</th>
                            <th scope="col" className="px-6 py-3">Подтверждено?</th>
                            <th scope="col" className="px-6 py-3">Когда добавлено</th>
                            <th scope="col" className="px-6 py-3"></th>
                        </tr>
                    </thead>
                    <tbody>
                        {invites.map((invite) => (
                            <tr className="border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200" key={invite.id}>
                                <td className="px-6 py-4">{ invite.id }</td>
                                <td className="px-6 py-4">{ invite.user_id }</td>
                                <td className="px-6 py-4">{ invite.interview_time }</td>
                                <td className="px-6 py-4">{ invite.confirmed ? "✅" : "❌"}</td>
                                <td className="px-6 py-4">{ invite.timestamp }</td>
                                <td className="px-6 py-4">
                                    <button
                                        onClick={() => handleDelete(invite.id)}
                                        className="text-red-500 hover:underline"
                                    >
                                       <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
  <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
</svg>
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="py-2.5 mb-2"><a href="http://localhost:8000/invites/export/csv" target="_blank" className="bg-gray-600 text-white px-4 py-2 rounded ">
  📤 Экспорт CSV</a></div>
            <button className="py-2.5 px-5 me-2 mb-2 flex items-center text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-4">
  <path strokeLinecap="round" strokeLinejoin="round" d="m18.75 4.5-7.5 7.5 7.5 7.5m-6-15L5.25 12l7.5 7.5" />
</svg>

                <a href="/" className="pl-2">Назад в главный меню</a>
            </button>
        </div>
    )
}

export default Invites