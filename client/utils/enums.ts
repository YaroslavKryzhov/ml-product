export const tableViews = ['Детально', 'Компактно', 'Подробнее', 'Матрица корреляции', 'Отбор признаков'];

export enum AppliedMethodTypes {
    DROP = 'Очистка данных',
    FILL = 'Заполнение пропусков',
    SCALE = 'Масштабирование данных',
    ENCODE = 'Кодирование данных'
}

export enum Methods {
    drop_duplicates = 'Удаление дубликатов',
    drop_na = 'Удаление пропусков',
    // drop_columns = 'Remove columns',
    fill_mean = 'Заполнение медианой',
    fill_median = 'Заполнение средним',
    fill_most_frequent = 'Заполнение модой',
    fill_custom_value = 'Заполнение заданным значением',
    fill_bfill = 'BackFill-заполнение',
    fill_ffill = 'ForwardFill-заполнение',
    fill_interpolation = 'Заполнение интерполяцией',
    fill_linear_imputer = 'Заполнение линейной моделью',
    fill_knn_imputer = 'Заполнение KNN-моделью',
    one_hot_encoding = 'One-Hot кодирование',
    ordinal_encoding = 'Порядковое кодирование',
    standard_scaler = 'Стандартизация (mean, scale)',
    min_max_scaler = 'Нормализация (min, max)',
    robust_scaler = 'Устойчивая стандартизация (median, quantiles)'
}

export enum ModelStatuses {
    Waiting,
    Building,
    Training,
    Trained,
    Problem
}

export enum ModelTaskTypes {
    classification,
    regression,
    clustering,
    outlier_detection,
    dimensionality_reduction
}