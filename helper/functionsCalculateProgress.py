def calculate_progress_percentage(approved_donors, target_amount):
    """
    Menghitung persentase kemajuan berdasarkan jumlah donor yang disetujui
    dan target jumlah donor.

    Parameters:
    approved_donors (int): Jumlah donor yang disetujui.
    target_amount (int): Target jumlah donor yang diinginkan.

    Returns:
    float: Persentase kemajuan, dikembalikan dalam rentang 0-100.
    """
    if target_amount == 0:
        return 0.0  # Tidak ada target, maka progress dianggap 0%
    
    progress_percentage = (approved_donors / target_amount) * 100
    return round(progress_percentage, 2)