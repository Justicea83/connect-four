import ApiService from '@/services/ApiService'

export default function useGame() {
    const getSingleGame = async (id) => {
        try {
            const resp = await ApiService.fetchData({
                url: `/api/game/games/${id}`,
                method: 'GET',
            })
            if (resp.data) {
                //console.log(resp.data)
                return {
                    status: 'success',
                    data: resp.data,
                }
            }
        } catch (e) {
            return {
                status: 'failed',
                message: 'sorry an error occurred',
            }
        }
    }

    return {
        getSingleGame,
    }
}